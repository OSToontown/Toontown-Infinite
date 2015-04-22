import json
import time
import os
import base64

from panda3d.core import URLSpec, HTTPClient, StringStream, DocumentSpec
from Crypto.Cipher import AES


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

        token = self.generateToken(700)
        if kwargs:
            kwargs['token'] = token
            self.send(kwargs)
        else:
            self.send((token,) + args)

    @staticmethod
    def generateToken(accessLevel):
        data = json.dumps({'timestamp': int(time.mktime(time.gmtime())),
                           'accesslevel': accessLevel})
        iv = os.urandom(AES.block_size)
        webRpcSecret = config.GetString('web-rpc-secret', '6163636f756e7473')
        cipher = AES.new(webRpcSecret, mode=AES.MODE_CBC, IV=iv)
        data += '\x00' * (16 - (len(data) % AES.block_size))
        token = cipher.encrypt(data)
        return base64.b64encode(iv + token)

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
