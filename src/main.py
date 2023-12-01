import re
from urllib.parse import urljoin
import logging
from collections import Counter

import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm
from prettytable import PrettyTable

from constants import BASE_DIR, MAIN_DOC_URL, PEPS_DOC_URL
from configs import configure_argument_parser, configure_logging
from outputs import control_output, file_outputs
from utils import get_response, find_tag, compare_statuses


def whats_new(session):
    """ Парсер обновления документации по Python. """
    what_new_url = urljoin(MAIN_DOC_URL, 'whatsnew/')
    response = get_response(session, what_new_url)
    if response is None:
        return
    soup = BeautifulSoup(response.text, features='lxml')
    main_div = find_tag(soup, 'section', attrs={'id': 'what-s-new-in-python'})
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    section_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, автор')]
    for section in tqdm(section_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(what_new_url, href)
        response = get_response(session, version_link)
        if response is None:
            continue
        soup = BeautifulSoup(response.text, features='lxml')
        h1 = find_tag(soup, 'h1').text
        dl = find_tag(soup, 'dl').text
        dl.replace('\n', ' ')
        results.append((version_link, h1, dl))

    return results


def latest_versions(session):
    """ Парсер версий Python и их состояния. """
    response = get_response(session, MAIN_DOC_URL)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    sidebar = find_tag(soup, 'div', {'class': 'sphinxsidebarwrapper'})
    ul_tags = sidebar.find_all('ul')
    for ul in ul_tags:
        if 'All version' in ul.text:
            a_tags = ul.find_all('a')
            break

    results = [('Ссылка на документацию', 'Версия', 'Статус')]
    pattern = r'Python (?P<version>\d\.\d+) \((?P<status>.*)\)'
    for a_tag in a_tags:
        link = a_tag['href']
        text_match = re.search(pattern, a_tag.text)
        if text_match is not None:
            version, status = text_match.groups()
        else:
            version, status = a_tag.text, ''
        results.append((link, version, status))

    return results


def download(session):
    """ Парсер архива Python. """
    download_urls = urljoin(MAIN_DOC_URL, 'download.html')
    response = get_response(session, download_urls)
    if response is None:
        return
    soup = BeautifulSoup(response.text, 'lxml')
    main_tag = find_tag(soup, 'div', {'role': 'main'})
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(download_urls, pdf_a4_link)
    filename = archive_url.split('/')[-1]

    downloads_dir = BASE_DIR / 'downloads'
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


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
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': parser_pep
}


def main():
    configure_logging()
    logging.info('Парсер запущен!')

    arg_parser = configure_argument_parser(MODE_TO_FUNCTION.keys())
    args = arg_parser.parse_args()
    logging.info(f'Аргументы командной строки: {args}')
    session = requests_cache.CachedSession()
    if args.clear_cache:
        session.cache.clear()
    parser_mode = args.mode
    results = MODE_TO_FUNCTION[parser_mode](session)
    if results is not None:
        control_output(results, args)
    logging.info('Парсер завершил работу. ')


if __name__ == "__main__":
    main()
