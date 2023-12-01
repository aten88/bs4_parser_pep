import logging
import argparse

from logging.handlers import RotatingFileHandler

from constants import BASE_DIR, LOG_FORMAT, DT_FORMAT


def configure_argument_parser(available_modes):
    """ Метод выюора режима работы парсера. """
    parser = argparse.ArgumentParser(description='Парсер документации PEP.')
    parser.add_argument(
       'mode',
       choices=available_modes,
       help='Режим работы парсера'
    )
    parser.add_argument(
        '-c',
        '--clear-cache',
        action='store_true',
        help='Очистка кеша'
    )
    return parser


def configure_logging():
    """ Метод логирования работы парсера. """
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
