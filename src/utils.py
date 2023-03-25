import logging
import os
from logger import init_logger

logger = init_logger(__name__, log_level=logging.INFO)


def parse_http(data: str):
    assert len(data) != 0, "data must be longer than 0 byte"
    splitted_data = data.split("\r\n")
    url, fname = extract_url_and_fname(splitted_data[0])
    host = extract_host(splitted_data[1])
    return url, fname, host


def get_content_from_response(http_message):
    splitted_msg = http_message.split("\r\n\r\n")
    content = splitted_msg[-1]
    return content.strip()


def get_status(http_message):
    splitted_msg = http_message.split("\r\n")
    pos = splitted_msg[0].find(" ")
    return splitted_msg[0][pos + 1:]


def extract_url_and_fname(request_message: str):
    url_start_pos = request_message.find(" ")
    url_end_pos = request_message.rfind(" ")
    url = request_message[url_start_pos + 1:url_end_pos]
    f_name = url.split("/")[-1]
    return url, f_name


def extract_host(request_message: str):
    colon_pos = request_message.find(" ")
    hostname = request_message[colon_pos + 1:]
    return hostname


def build_download_request(url, host):
    request = f"GET {url} HTTP/1.1\r\n"\
            + f"Host: {host}\r\n"\
            + "Accept: text/html\r\n\r\n"
    return bytes(request, "ascii")


def write_content_to_disk(http_message, fname):
    content = get_content_from_response(http_message)
    if fname in os.listdir(os.getcwd()):
        logger.info(f"File {fname} already exists... Overwriting")
    with open(fname, "w", encoding="utf-8") as fout:
        fout.write(content)
