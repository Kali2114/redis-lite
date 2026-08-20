import threading


class Store:
    def __init__(self):
        self.data = {}
        self.lock = threading.Lock()

    def get(self, key):
        with self.lock:
            return self.data.get(key)

    def set(self, key, value):
        with self.lock:
            self.data[key] = value
            return True

    def delete(self, key):
        with self.lock:
            if key in self.data:
                del self.data[key]
                return True
            return False