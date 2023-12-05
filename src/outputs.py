import csv
import datetime as dt
import logging
from collections import Counter

from prettytable import PrettyTable

from constants import (
    BASE_DIR, DATETIME_FORMAT,
    RESULTS_DIRECTORY, DEFAULT_ENCODING,
    PRETTY_MODE, FILE_MODE
)
from configs import configure_logging


def control_output(results, cli_args, total=None):
    """ Метод вариантов вывода данных """
    output = cli_args.output

    if output == PRETTY_MODE:
        pretty_output(results, total)
    elif output == FILE_MODE:
        file_output(results, cli_args, total)
    else:
        default_outputs(results, total)


def default_outputs(results, total):
    """ Вывод данных без аргументов """
    if isinstance(total, int):
        for row in results[0]:
            print(*row)
    else:
        for row in results:
            print(*row)


def pretty_output(results, total):
    """ Вывод данных в формате Prettytable """
    if isinstance(total, int):
        status_count = Counter(results[0])
        table = PrettyTable()
        table.field_names = ['Статус', 'Количество']
        for status, count in sorted(status_count.items()):
            table.add_row([status, count])
        table.add_row(['----------', '----------'])
        table.add_row(['Total', total])
        print(table)
    else:
        table = PrettyTable()
        table.field_names = results[0]
        table.align = 'l'
        table.add_rows(results[1:])
        print(table)


def file_output(results, cli_args, total):
    """ Создание файла csv Python/PEP """
    results_dir = BASE_DIR / RESULTS_DIRECTORY
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    if isinstance(total, int):
        configure_logging()
        count_results = Counter(results[0])
        with open(file_path, 'w', newline='', encoding=DEFAULT_ENCODING) as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerow(['Статус', 'Количество'])
            for status, count in count_results.items():
                writer.writerow([status, count])
            writer.writerow(['Total', total])
        logging.info(f'Парсер создал файл: {file_path}')
    else:
        with open(file_path, 'w', encoding=DEFAULT_ENCODING) as f:
            writer = csv.writer(f, dialect='unix')
            writer.writerows(results)
        logging.info(f'Файл с результатами был сохранён: {file_path}')
