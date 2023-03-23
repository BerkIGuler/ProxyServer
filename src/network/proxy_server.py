from logger import init_logger
import socket


class ProxyServer:
    def __init__(self, host_ip, port):
        self.logger = init_logger(__name__)
        self.host_ip = host_ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket = None
        self.listening_addr = None

    def bind(self):
        self.server_socket.bind((self.host_ip, self.port))

    def listen(self):
        self.server_socket.listen()

    def accept(self):
        self.listening_socket, self.listening_addr = self.server_socket.accept()

    def receive_msg(self, size=1024):
        if self.listening_socket:
            message = self.listening_socket.recv(size)
            return message.decode("utf-8")
        else:
            raise ConnectionRefusedError("listening socket not created yet...")

    def close_conn(self):
        self.server_socket.close()
        if self.listening_socket:
            self.listening_socket.close()
