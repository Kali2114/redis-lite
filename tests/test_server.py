import threading
import socket
from tests.conftest import send_command, send_set_command


def test_get_missing_key_returns_nil(server_port):
    response = send_command(server_port, 'GET name')
    assert response == b'(nil)\n'


def test_get_existing_key_returns_value(server_port):
    send_set_command(server_port, 'name', 'Kamil')
    response = send_command(server_port, 'GET name')
    assert response == b'5\r\nKamil'


def test_set_key_return_ok(server_port):
    response = send_set_command(server_port, 'name', 'Kamil')
    assert response == b'OK\n'


def test_delete_missing_key_returns_0(server_port):
    response = send_command(server_port, 'DEL name')
    assert response == b'0\n'


def test_delete_existing_key_returns_1(server_port):
    send_set_command(server_port, 'name', 'Kamil')
    response = send_command(server_port, 'DEL name')
    assert response == b'1\n'


def test_unknown_command(server_port):
    response = send_command(server_port, 'SIL name')
    assert response == b'SIL unknown command\n'


def test_empty_command(server_port):
    response = send_command(server_port, '')
    assert response == b'ERR empty command\n'


def test_get_value_with_embedded_newline(server_port):
    send_set_command(server_port, 'note', 'line one\r\nline two')
    response = send_command(server_port, 'GET note')
    assert response == b'18\r\nline one\r\nline two'


def test_many_clients(server_port):
    results = []

    def worker(i):
        key = f"key{i}"
        value = f"value{i}"
        send_set_command(server_port, key, value)
        response = send_command(server_port, f'GET {key}')
        results.append((i, response))

    threads = []

    for i in range(10):
        thread = threading.Thread(target=worker, args=(i,))
        threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    assert len(results) == 10
    for i, response in results:
        value = f"value{i}"
        length = len(value.encode("utf-8"))
        expected = f"{length}\r\n{value}"
        expected = expected.encode("utf-8")
        assert response == expected


def test_idle_client_not_block_other(server_port):
    idle_client = socket.create_connection(("localhost", server_port))
    response = send_command(server_port, 'GET name')
    idle_client.close()
    assert response == b'(nil)\n'



