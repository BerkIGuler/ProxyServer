from logger import init_logger
import socket


class ProxyServer:
    def __init__(self, host_ip, port):
        self.logger = init_logger(__name__, log_level="INFO")
        self.host_ip = host_ip
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listening_socket = None
        self.listening_addr = None

    def bind(self):
        self.server_socket.bind((self.host_ip, self.port))
        self.logger.debug(
            f"Successfully binded to the IP:{self.host_ip} port:{self.port}"
        )

    def listen(self):
        self.server_socket.listen()
        self.logger.debug(
            f"Listening new connections at IP:{self.host_ip} port:{self.port}"
        )

    def accept(self):
        self.listening_socket, self.listening_addr = self.server_socket.accept()
        self.logger.debug(
            f"New connection accepted from {self.listening_addr}"
        )

    def receive_msg(self, size=1024):
        if self.listening_socket:
            message = self.listening_socket.recv(size)
            self.logger.debug(
                f"Received message of size {len(message)}"
            )
            return message.decode("utf-8").strip()
        else:
            raise ConnectionRefusedError("listening socket not created yet...")

    def respond_content(self, body, content_type):
        headers = "HTTP/1.1 200 OK\r\n"\
                  + f"Content-Type: text/{content_type}\r\n"\
                  + f"Content-Length: {len(body)}\r\n\r\n"
        response = headers + body
        response = bytes(response, "utf-8")
        if self.listening_socket:
            self.listening_socket.sendall(response)
        else:
            raise ConnectionRefusedError("listening socket not created yet...")

    def close_conn(self):
        self.server_socket.close()
        if self.listening_socket:
            self.listening_socket.close()
