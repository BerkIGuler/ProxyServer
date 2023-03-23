import argparse

from logger import init_logger
from network import ProxyServer, WebClient
from network.utils import parse_http, get_content_from_response, get_status


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="HTTP Proxy Server"
    )

    parser.add_argument(
        "port",
        type=int,
        help="The Proxy server port that your program will be listening to."
    )

    args = parser.parse_args()
    logger = init_logger(__name__, log_level="DEBUG")

    proxy_server = ProxyServer(host_ip="127.0.0.1", port=args.port)
    proxy_server.bind()
    proxy_server.listen()
    proxy_server.accept()
    msg = proxy_server.receive_msg()

    print("Retrieved request from Firefox:\n")
    print(msg, end="\n\n")

    url, fname, host = parse_http(msg)
    print(f"Downloading file '{fname}'...")
    client = WebClient(hostname=host, port=80)
    down_content = client.download_file(url)

    print(get_content_from_response(down_content))
    print(get_status(down_content))
