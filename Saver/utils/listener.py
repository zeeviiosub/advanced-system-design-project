from utils.connection import Connection


class Listener:
    def __init__(self, port, host='0.0.0.0', backlog=1000, reuseaddr=True):
        self.port = port
        self.host = host
        self.backlog = backlog
        self.reuseaddr = reuseaddr

    def __repr__(self):
        return f"Listener(port={self.port}, host='{self.host}'," + \
            f"backlog={self.backlog}, reuseaddr={self.reuseaddr})"

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, x, y, z):
        self.stop()

    def start(self):
        import socket
        self.server = socket.socket()
        if self.reuseaddr:
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((self.host, self.port))
        self.server.listen(self.backlog)

    def stop(self):
        self.server.close()

    def accept(self):
        return Connection(self.server.accept()[0])
