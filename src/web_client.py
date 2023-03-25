import socket
from utils import build_download_request
from logger import init_logger


class WebClient:
    def __init__(self, hostname, port=80):
        self.logger = init_logger(__name__, log_level="INFO")
        self.hostname = hostname
        self.host_ip = self._get_ip(hostname)
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _connect(self):
        self.client_socket.connect((self.host_ip, self.port))
        self.logger.debug(
            f"Connected to IP:{self.host_ip} port:{self.port}"
        )

    def _send(self, message):
        self.client_socket.sendall(message)
        self.logger.debug(
            f"Sent GET request to IP:{self.host_ip} port:{self.port}"
        )

    def _receive_resp(self):
        resp = bytes()
        while True:
            resp_chunk = self.client_socket.recv(1024)
            if not resp_chunk:
                break
            resp = resp + resp_chunk

        self.logger.debug(
            f"Received a file of size {len(resp)} from {self.host_ip}"
        )
        return resp.decode("utf-8")

    def download_file(self, url):
        self._connect()
        message = build_download_request(url, self.hostname)
        self._send(message)
        return self._receive_resp()

    def close_conn(self):
        self.client_socket.close()

    def _get_ip(self, name):
        try:
            ip_addr = socket.gethostbyname(name)
            return ip_addr
        except socket.gaierror:
            self.logger.debug(
                "Could not resolve ip from hostname, "
                "will use hostname instead"
            )
            return name
