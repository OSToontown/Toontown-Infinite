from toontown.util.ThreadedCall import ThreadedCall
import time

class BulkLoader:

    def __init__(self, modelPaths):
        self.modelPaths = modelPaths
        self.modelPool = {}

    def load(self):
        threads = []
        for modelPath in self.modelPaths:
            t = ThreadedCall(loader.loadModel, args=(modelPath,), callback=self.modelDone, callbackArgs=(modelPath,))
            threads.append(t)

        waitUntilDone = ThreadedCall(self.waitUntilDone)
        threads.append(waitUntilDone)
        for t in threads:
            t.start()
            t.join()

    def waitUntilDone(self):
        while len(self.modelPool) != len(self.modelPaths):
            time.sleep(0.01)

    def modelDone(self, model, modelPath):
        self.modelPool[modelPath] = model

    def unload(self):
        for model in self.modelPool.values():
            if not model.isEmpty():
                model.removeNode()

        self.modelPool = {}

    def getModel(self, modelPath):
        return self.modelPool.get(modelPath)