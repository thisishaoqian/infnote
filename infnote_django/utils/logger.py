import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    file_handlder = logging.FileHandler('/tmp/infnote.log')
    file_handlder.setLevel(logging.DEBUG)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('[%(asctime)s][%(name)s][%(levelname)s] %(message)s')
    file_handlder.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handlder)
    logger.addHandler(stream_handler)

    return logger
