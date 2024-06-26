import re
from urllib.parse import urljoin
import logging
from collections import defaultdict

import requests_cache
from tqdm import tqdm

from constants import (
    BASE_DIR, MAIN_DOC_URL,
    PEPS_DOC_URL, EXPECTED_STATUS,
    WHATS_NEW_ENDPOINT, DOWNLOAD_ENDPOINT,
    DOWNLOADS_DIR
)
from configs import configure_argument_parser, configure_logging
from outputs import control_output
from utils import find_tag, get_soup


def whats_new(session):
    """ Парсер обновления документации по Python """
    what_new_url = urljoin(MAIN_DOC_URL, WHATS_NEW_ENDPOINT)
    main_div = find_tag(
        get_soup(session, what_new_url, features='lxml'),
        'section',
        attrs={'id': 'what-s-new-in-python'}
    )
    div_with_ul = find_tag(main_div, 'div', attrs={'class': 'toctree-wrapper'})
    section_by_python = div_with_ul.find_all(
        'li', attrs={'class': 'toctree-l1'}
    )
    results = [('Ссылка на статью', 'Заголовок', 'Редактор, Автор')]
    for section in tqdm(section_by_python):
        version_a_tag = find_tag(section, 'a')
        href = version_a_tag['href']
        version_link = urljoin(what_new_url, href)
        h1 = find_tag(
            get_soup(session, version_link, features='lxml'), 'h1'
        ).text
        dl = find_tag(
            get_soup(session, version_link, features='lxml'), 'dl'
        ).text
        dl.replace('\n', ' ')
        results.append((version_link, h1, dl))

    return results


def latest_versions(session):
    """ Парсер версий Python и их состояния """
    sidebar = find_tag(
        get_soup(session, MAIN_DOC_URL, 'lxml'),
        'div', {'class': 'sphinxsidebarwrapper'}
    )
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
    """ Парсер архива Python """
    download_urls = urljoin(MAIN_DOC_URL, DOWNLOAD_ENDPOINT)
    main_tag = find_tag(
        get_soup(session, download_urls, 'lxml'), 'div', {'role': 'main'}
    )
    table_tag = find_tag(main_tag, 'table', {'class': 'docutils'})
    pdf_a4_tag = find_tag(
        table_tag, 'a', {'href': re.compile(r'.+pdf-a4\.zip$')}
    )
    pdf_a4_link = pdf_a4_tag['href']
    archive_url = urljoin(download_urls, pdf_a4_link)
    filename = archive_url.split('/')[-1]

    downloads_dir = BASE_DIR / DOWNLOADS_DIR
    downloads_dir.mkdir(exist_ok=True)
    archive_path = downloads_dir / filename
    response = session.get(archive_url)
    with open(archive_path, 'wb') as file:
        file.write(response.content)
    logging.info(f'Архив был загружен и сохранён: {archive_path}')


def pep(session):
    """ Метод получения статусов PEP """
    num_index_section = get_soup(session, PEPS_DOC_URL, 'lxml').find(
        'section', attrs={'id': 'numerical-index'}
    )
    peps_body_table = num_index_section.find('tbody')
    peps_tr = peps_body_table.find_all('tr')

    statuses_count = defaultdict(int)
    configure_logging()

    for pep_a in tqdm(peps_tr):
        name_pep = pep_a.find('a')
        td_pep = pep_a.find('td')
        abbr_pep = td_pep.find('abbr')
        status_pep_general = abbr_pep.text[1:]

        href = name_pep['href']
        pep_link = urljoin(PEPS_DOC_URL, href)
        status_in_card_pep = get_soup(
            session, pep_link, 'lxml'
        ).find('abbr').text

        expected_status = EXPECTED_STATUS.get(status_pep_general)
        if expected_status is None:
            logging.error(
                f'\n'
                f'{pep_link}\n'
                f'Статус в карточке: {status_pep_general}'
                f'Ожидаемые статусы: {status_in_card_pep}'
            )
            continue

        if status_in_card_pep in expected_status:
            statuses_count[status_in_card_pep] += 1
        else:
            logging.error(
                f'\n'
                f'Несовпадающие статусы:\n'
                f'{pep_link}\n'
                f'Статус в карточке: {status_in_card_pep}\n'
                f'Ожидаемые статусы: {expected_status}\n'
            )

    results = [('Статус', 'Количество')]
    for status, count in statuses_count.items():
        results.append((status, count))

    total_count = len(peps_tr)
    results.append(('Total', total_count))

    return results


MODE_TO_FUNCTION = {
    'whats-new': whats_new,
    'latest-versions': latest_versions,
    'download': download,
    'pep': pep
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
    try:
        results = MODE_TO_FUNCTION[parser_mode](session)
        if results is not None:
            control_output(results, args)
    except Exception as e:
        logging.exception(
            f'Ошибка в работе парсера {e}'
        )
    logging.info('Парсер завершил работу. ')


if __name__ == "__main__":
    main()
