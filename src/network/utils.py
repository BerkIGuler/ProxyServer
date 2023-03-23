
def parse_http(data: str):
    assert len(data) != 0, "data must be longer than 0 byte"
    splitted_data = data.split("\r\n")
    url, fname = extract_url_and_fname(splitted_data[0])
    host = extract_host(splitted_data[1])
    return url, fname, host


def get_content_from_response(http_message):
    splitted_msg = http_message.split("\r\n\r\n")
    return splitted_msg[-1]


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
