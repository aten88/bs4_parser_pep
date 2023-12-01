import logging
from urllib.parse import urljoin
from collections import Counter

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm
from prettytable import PrettyTable

from constants import PEPS_DOC_URL
from utils import compare_statuses
from outputs import file_outputs
from configs import configure_argument_parser, configure_logging


def parser_pep(session):
    configure_logging()
    logging.info('Парсер запущен!')
    response = session.get(PEPS_DOC_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    num_index_section = soup.find('section', attrs={'id': 'numerical-index'})
    peps_body_table = num_index_section.find('tbody')
    peps_tr = peps_body_table.find_all('tr')

    compare_list_statuses = []

    for pep_a in tqdm(peps_tr):
        name_pep = pep_a.find('a')
        td_pep = pep_a.find('td')
        abbr_pep = td_pep.find('abbr')
        status_pep_general = abbr_pep.text[1:]

        href = name_pep['href']
        pep_link = urljoin(PEPS_DOC_URL, href)
        response_link = session.get(pep_link)
        response_link.encoding = 'utf-8'
        soup = BeautifulSoup(response_link.text, 'lxml')

        status_in_card_pep = soup.find('abbr').text
        compare_list_statuses.append({status_pep_general: {
                    'pep_link': pep_link,
                    'status_in_card': status_in_card_pep
                }}
        )

    status_count = Counter(compare_statuses(compare_list_statuses))
    total_peps = len(compare_list_statuses)
    table = PrettyTable()
    table.field_names = ['Статус', 'Количество']
    for status, count in sorted(status_count.items()):
        table.add_row([status, count])
    table.add_row(['----------', '----------'])
    table.add_row(['Total', total_peps])
    file_outputs(dict(status_count), total_peps)
    print(table)
    logging.info('Парсер завершил работу!')


MODE_TO_FUNCTION = {
    'pep': parser_pep
}


def main():
    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    MODE_TO_FUNCTION[parser_mode](session)


if __name__ == '__main__':
    main()
