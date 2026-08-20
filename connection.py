class Connection:
    def __init__(self, client_socket):
        self.client_socket = client_socket
        self.buffer = b''


    def read_line(self):
        while b"\r\n" not in self.buffer:
            chunk = self.client_socket.recv(1024)
            if not chunk:
                raise ConnectionError("client disconnected")
            self.buffer += chunk
        index = self.buffer.find(b"\r\n")
        line = self.buffer[:index]
        self.buffer = self.buffer[index+2:]
        return line
