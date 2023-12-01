import csv
import datetime as dt
import logging

from prettytable import PrettyTable

from constants import BASE_DIR, DATETIME_FORMAT
from configs import configure_logging


def control_output(results, cli_args):
    output = cli_args.output

    if output == 'pretty':
        pretty_output(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_outputs(results)


def default_outputs(results):

    for row in results:
        print(*row)


def pretty_output(results):

    table = PrettyTable()
    table.field_names = results[0]
    table.align = 'l'
    table.add_rows(results[1:])
    print(table)


def file_output(results, cli_args):
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    parser_mode = cli_args.mode
    now = dt.datetime.now()
    now_formatted = now.strftime(DATETIME_FORMAT)
    file_name = f'{parser_mode}_{now_formatted}.csv'
    file_path = results_dir / file_name
    with open(file_path, 'w', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerows(results)
    logging.info(f'Файл с результатами был сохранён: {file_path}')


def file_outputs(data, total):
    """ Метод вывода данных PEP. """
    configure_logging()
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    file_name = results_dir / 'status_table.csv'
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerow(['Статус', 'Количество'])
        for status, count in data.items():
            writer.writerow([status, count])
        writer.writerow(['Total', total])
        logging.info(f'Парсер создал файл: {file_name}')
