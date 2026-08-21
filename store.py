import threading
from node import Node


class Store:
    def __init__(self, max_size=10):
        self.data = {}
        self.lock = threading.Lock()
        self.head = Node(None, None)
        self.tail = Node(None, None)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.max_size = max_size

    def get(self, key):
        with self.lock:
            node = self.data.get(key)
            if node is None:
                return None
            self._move_to_front(node)
            return node.value

    def set(self, key, value):
        with self.lock:
            if key in self.data:
                node = self.data[key]
                node.value = value
                self._move_to_front(node)
                return True
            new_node = Node(key, value)
            self.data[key] = new_node
            self._add_node(new_node)
            if len(self.data) > self.max_size:
                lru_node = self.tail.prev
                self._remove_node(lru_node)
                del self.data[lru_node.key]
            return True

    def delete(self, key):
        with self.lock:
            if key in self.data:
                node = self.data.pop(key)
                self._remove_node(node)
                return True
            return False

    def _add_node(self, node):
        first = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = first
        first.prev = node

    def _remove_node(self, node):
        node.prev.next = node.next
        node.next.prev = node.prev

    def _move_to_front(self, node):
        self._remove_node(node)
        self._add_node(node)
