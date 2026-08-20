import socket
from connection import Connection
from threading import Thread


class Server:
    def __init__(self, host, port, store):
        self.host = host
        self.port = port
        self.store = store
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _handle_get(self, parts):
            response = self.store.get(parts[1])
            if response is None:
                response = b"(nil)\n"
                return response
            else:
                response = response.encode("utf-8")
                length = len(response)
                length_prefix = f"{length}\r\n".encode("utf-8")
                response = length_prefix + response
                return response

    def _handle_set(self, parts, connection):
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
        return response

    def handle_client(self, client_socket):
        try:
            connection = Connection(client_socket)
            line = connection.read_line()
            parts = line.decode("utf-8").split()
            response = None
            if len(parts) == 2 and parts[0] == "GET":
                response = self._handle_get(parts)
                client_socket.sendall(response)
                client_socket.close()
                return
            elif len(parts) == 3 and parts[0] == "SET":
                response = self._handle_set(parts, connection)
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
            client_socket.sendall(response)
            return
        except ConnectionError:
            return
        finally:
            client_socket.close()

    def start(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        while True:
            client_socket, client_address = self.socket.accept()
            Thread(target=self.handle_client, args=(client_socket,),daemon=True).start()


