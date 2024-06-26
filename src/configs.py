import logging
from logging.handlers import RotatingFileHandler
import argparse

from constants import (
    BASE_DIR, LOG_FORMAT,
    DATETIME_FORMAT, LOGS_DIRECTORY,
    LOG_FILENAME, DEFAULT_ENCODING,
    PRETTY_MODE, FILE_MODE
)


def configure_argument_parser(available_modes):
    """ Конфигуратор аргументов командной строки """
    parser = argparse.ArgumentParser(description="Парсер документации Python.")
    parser.add_argument(
        'mode', choices=available_modes, help='Режимы работы парсера'
    )
    parser.add_argument(
        '-c', '--clear-cache',
        action='store_true', help='Очистка кеша'
    )
    parser.add_argument(
        '-o', '--output',
        choices=(PRETTY_MODE, FILE_MODE),
        help='Дополнительные способы вывода данных'
    )
    return parser


def configure_logging():
    """ Конфигуратор логов """
    log_dir = BASE_DIR / LOGS_DIRECTORY
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / LOG_FILENAME
    rotating_handler = RotatingFileHandler(
        log_file, maxBytes=10 ** 6,
        backupCount=5, encoding=DEFAULT_ENCODING
    )
    logging.basicConfig(
        datefmt=DATETIME_FORMAT, format=LOG_FORMAT,
        level=logging.INFO,
        handlers=(rotating_handler, logging.StreamHandler())
    )
