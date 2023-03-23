import socket
from network.utils import build_download_request
from logger import init_logger


class WebClient:
    def __init__(self, hostname, port=80):
        self.logger = init_logger(__name__, log_level="DEBUG")
        self.hostname = hostname
        self.host_ip = self._get_ip(hostname)
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _connect(self):
        self.client_socket.connect((self.host_ip, self.port))

    def _send(self, message):
        self.client_socket.sendall(message)

    def _receive_resp(self):
        resp = self.client_socket.recv(1024)
        return resp.decode("utf-8")

    def download_file(self, url):
        self._connect()
        message = build_download_request(url, self.hostname)
        self._send(message)
        return self._receive_resp()

    def close_conn(self):
        self.client_socket.close()

    @staticmethod
    def _get_ip(name):
        return socket.gethostbyname(name)
