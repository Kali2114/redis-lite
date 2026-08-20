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


