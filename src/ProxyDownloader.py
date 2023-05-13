import argparse
import os

from logger import init_logger
from proxy_server import ProxyServer
from web_client import WebClient
from utils import (parse_http,
                   get_status,
                   write_content_to_disk,
                   get_content_from_response)


def parse_args():
    parser = argparse.ArgumentParser(
        description="HTTP Proxy Server"
    )
    parser.add_argument(
        "port",
        type=int,
        help="The Proxy server port that your program will be listening to."
    )

    args = parser.parse_args()
    return args


if __name__ == "__main__":

    args = parse_args()
    logger = init_logger(__name__, log_level="INFO")
    LOCAL_HOST = "127.0.0.1"
    WEB_SERVER_PORT = 80

    proxy_server = ProxyServer(host_ip=LOCAL_HOST, port=args.port)
    proxy_server.bind()
    proxy_server.listen()

    while True:
        proxy_server.accept()
        msg = proxy_server.receive_msg()

        url, fname, host = parse_http(msg)

        # filter out firefox related queries
        if "bilkent" not in host:
            continue

        print("Retrieved request from Firefox:\n")
        print(msg, end="\n\n")

        print(f"Downloading file '{fname}'...")
        client = WebClient(hostname=host, port=WEB_SERVER_PORT)
        down_content = client.download_file(url)

        status = get_status(down_content)
        if status == "200 OK":
            print(f"Retrieved: {status}")
            content = get_content_from_response(down_content)
            proxy_server.respond_content(body=content, content_type="plain")
            print("saving file...")
            write_content_to_disk(down_content, fname)
            print(f"Successfully saved into {os.path.join(os.getcwd(), fname)}...")
        else:
            print(f"Could not retrieve: {status}")
            print("Error: File could not be downloaded")
            content = get_content_from_response(down_content)
            proxy_server.respond_content(body=content, content_type="html")
