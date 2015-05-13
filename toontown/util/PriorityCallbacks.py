import bisect


class PriorityCallbacks:
    def __init__(self):
        self.callbacks = []

    def add(self, callback, priority=0):
        item = (priority, callback)
        bisect.insort(self.callbacks, item)
        return item

    def remove(self, item):
        self.callbacks.pop(bisect.bisect_left(self.callbacks, item))

    def clear(self):
        self.callbacks = []

    def __call__(self):
        for _, callback in self.callbacks:
            callback()
