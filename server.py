import socket
from connection import Connection


class Server:
    def __init__(self, host, port, store):
        self.host = host
        self.port = port
        self.store = store
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def handle_client(self, client_socket):
        connection = Connection(client_socket)
        line = connection.read_line()
        parts = line.decode("utf-8").split()
        response = None
        if len(parts) == 2 and parts[0] == "GET":
            response = self.store.get(parts[1])
            if response is None:
                response = "(nil)"
            else:
                response = response.encode("utf-8")
                length = len(response)
                length_prefix = f"{length}\r\n".encode("utf-8")
                response = length_prefix + response
                return response
        elif len(parts) == 3 and parts[0] == "SET":
            length = int(parts[2])
            value = connection.read_exact(length)
            try:
                value = value.decode("utf-8")
            except UnicodeDecodeError:
                response = "ERR invalid utf-8"
            else:
                connection.read_line()
                self.store.set(parts[1], value)
                response = "OK"
        elif len(parts) == 2 and parts[0] == "DEL":
            response = self.store.delete(parts[1])
            response = "1" if response else "0"
        if response is None:
            if parts:
                response = (f"{parts[0]} unknown command")
            else:
                response = "ERR empty command"
        response = str(response) + "\n"
        response = response.encode("utf-8")
        return response



    def start(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        while True:
            client_socket, client_address = self.socket.accept()
            response = self.handle_client(client_socket)
            client_socket.sendall(response)
            client_socket.close()



