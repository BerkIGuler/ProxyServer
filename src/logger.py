import logging

logging.root.setLevel(logging.NOTSET)


def init_logger(
        logger_name,
        log_level="INFO",
        log_path="server_logs.log"):

    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    f_handler = logging.FileHandler(log_path)
    format_ = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    if log_level == "INFO":
        f_handler.setLevel(logging.INFO)
    elif log_level == "DEBUG":
        f_handler.setLevel(logging.DEBUG)
        c_handler = logging.StreamHandler()
        c_handler.setLevel(logging.DEBUG)
        c_handler.setFormatter(format_)
        logger.addHandler(c_handler)

    f_handler.setFormatter(format_)
    logger.addHandler(f_handler)

    return logger
