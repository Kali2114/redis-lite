import threading
import time

import pytest

from store import Store
import socket
from server import Server


@pytest.fixture
def server_port():
    store = Store()
    server = Server("127.0.0.1", 0, store)
    thread = threading.Thread(target=server.start, daemon=True)
    thread.start()
    time.sleep(0.1)
    yield server.socket.getsockname()[1]


def send_command(port, command, timeout=2):
    with socket.create_connection(("localhost", port), timeout=timeout) as client:
        client.sendall(command.encode() + b"\n")
        return client.recv(1024)