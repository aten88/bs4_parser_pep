import logging

from logging.handlers import RotatingFileHandler

from constants import BASE_DIR, LOG_FORMAT, DT_FORMAT


def configure_logging():
    log_dir = BASE_DIR / 'logs'
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / 'bs4parser.log'
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6,
        backupCount=10, encoding='utf-8'
    )
    logging.basicConfig(
        datefmt=DT_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
