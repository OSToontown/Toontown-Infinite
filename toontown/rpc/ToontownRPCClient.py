import json

from panda3d.core import URLSpec, HTTPClient, StringStream, DocumentSpec


class ProtocolError(Exception):
    pass


class ToontownRPCClient:
    notify = directNotify.newCategory('ToontownRPCClient')

    def __init__(self, endpoint):
        self.url = URLSpec(endpoint)

        self.http = HTTPClient()
        self.http.setVerifySsl(0)

        self.channels = {}

        # Start polling:
        taskName = self.getUniqueName() + '-pollTask'
        taskMgr.add(self.pollTask, taskName)

    def __getattr__(self, item):
        return ToontownRPCMethod(self, item)

    def getUniqueName(self):
        return 'ToontownRPCClient-' + str(id(self))

    def pollOnce(self):
        for channel, method in self.channels.items():
            if not channel.run():
                del self.channels[channel]
                method.finish()

    def pollTask(self, task):
        self.pollOnce()
        return task.cont


class ToontownRPCMethod:
    def __init__(self, client, name):
        self.client = client
        self.name = name

        self.notify = directNotify.newCategory('ToontownRPCMethod[%s]' % name)

        self.channel = None
        self.stream = StringStream()
        self.callback = None
        self.errback = None

    def __call__(self, *args, **kwargs):
        self.callback = kwargs.pop('_callback', None)
        self.errback = kwargs.pop('_errback', None)

        if (len(args) > 0) and (len(kwargs) > 0):
            raise ProtocolError('Cannot use both positional and keyword arguments.')

        self.send(args if len(args) > 0 else kwargs)

    def send(self, params):
        if not self.client.url.hasServer():
            if self.errback is not None:
                self.errback()
            return

        self.channel = self.client.http.makeChannel(False)

        self.channel.sendExtraHeader('Accept', 'application/json')
        self.channel.sendExtraHeader('Content-Type', 'application/json')
        self.channel.sendExtraHeader('User-Agent', 'TTI-RPCClient/0.1')

        data = json.dumps({'jsonrpc': '2.0', 'method': self.name,
                           'params': params, 'id': id(self)})

        ds = DocumentSpec(self.client.url)

        self.channel.beginPostForm(ds, data)
        self.channel.downloadToStream(self.stream)

        self.client.channels[self.channel] = self

    def finish(self):
        if not self.channel.isValid():
            self.notify.warning('Failed to make HTTP request.')
            if self.errback is not None:
                self.errback()
            return

        if not self.channel.isDownloadComplete():
            self.notify.warning('Received an incomplete response.')
            if self.errback is not None:
                self.errback()
            return

        data = self.stream.getData()
        try:
            response = json.loads(data)
        except ValueError:
            self.notify.warning('Received an invalid response.')
            if self.errback is not None:
                self.errback()
            return

        error = response.get('error')
        if error is not None:
            self.notify.warning('Resulted in error: ' + repr(error))
            if self.errback is not None:
                self.errback()
            return

        if self.callback:
            self.callback(response['result'])
