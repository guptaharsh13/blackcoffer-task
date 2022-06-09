import os
from pathlib import Path
from dotenv import dotenv_values
from datetime import datetime
import logging


u_format = "[%(asctime)s]\t%(name)s | Line number - %(lineno)d | %(levelname)s | %(message)s"


def configLogger(name, filename="app.log"):

    u_format = logging.Formatter(
        "[%(asctime)s]\t%(name)s | Line number - %(lineno)d | %(levelname)s | %(message)s")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename)
    f_handler.setLevel(logging.INFO)

    c_handler.setFormatter(u_format)
    f_handler.setFormatter(u_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
