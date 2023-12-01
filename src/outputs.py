import csv
import datetime as dt
import logging

from prettytable import PrettyTable
from src.constants import BASE_DIR, DATETIME_FORMAT


def control_output(results, cli_args):
    output = cli_args.output

    if output == 'pretty':
        pretty_outputs(results)
    elif output == 'file':
        file_output(results, cli_args)
    else:
        default_outputs(results)


def default_outputs(results):

    for row in results:
        print(*row)


def pretty_outputs(results):

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
