class Connection:
    def __init__(self, socket):
        self.socket = socket

    def __repr__(self):
        sockname = self.socket.getsockname()
        fromaddr = f'{sockname[0]}:{sockname[1]}'
        peername = self.socket.getpeername()
        toaddr = f'{peername[0]}:{peername[1]}'
        return f'<Connection from {fromaddr} to {toaddr}>'

    def __enter__(self):
        return self

    def __exit__(self, x, y, z):
        self.close()

    def connect(host, port):
        import socket
        socket = socket.socket()
        socket.connect((host, port))
        return Connection(socket)

    def send(self, data):
        self.socket.sendall(data)

    def receive(self, size):
        data = self.socket.recv(size)
        while len(data) < size:
            more_data = self.socket.recv(size-len(data))
            if not more_data:
                raise Exception('Incomplete message')
            data += more_data
        return data

    def send_message(self, data):
        self.socket.sendall(len(data).to_bytes(8, 'little'))
        self.socket.sendall(data)

    def receive_message(self):
        size = int.from_bytes(self.socket.recv(8), 'little')
        data = self.socket.recv(size)
        while len(data) < size:
            more_data = self.socket.recv(size-len(data))
            if not more_data:
                raise Exception('Incomplete message')
            data += more_data
        return data

    def close(self):
        self.socket.close()
