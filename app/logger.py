import logging
import sys


def logger_factory(name: str = "Trading-Automation") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler("trading_automation.log", mode='a')
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(name)s: %(asctime)s | %(levelname)s | %(filename)s:%(lineno)d | %(process)d >>> %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.handlers.clear()

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger
