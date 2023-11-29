from urllib.parse import urljoin
import requests_cache
from bs4 import BeautifulSoup
from tqdm import tqdm
from prettytable import PrettyTable
from collections import Counter

from constants import PEPS_DOC_URL
from utils import compare_statuses


if __name__ == '__main__':

    session = requests_cache.CachedSession()
    response = session.get(PEPS_DOC_URL)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')

    num_index_section = soup.find('section', attrs={'id': 'numerical-index'})
    peps_body_table = num_index_section.find('tbody')
    peps_tr = peps_body_table.find_all('tr')

    compare_list_statuses = []
    in_card_statuses = []

    for pep_a in tqdm(peps_tr):
        name_pep = pep_a.find('a')
        title_name_general = name_pep['title'].split(' – ')[0]  # Название PEP
        # из внешней таблицы

        td_pep = pep_a.find('td')
        abbr_pep = td_pep.find('abbr')
        status_pep_general = abbr_pep.text[1:]  # Статус PEP из общей таблицы

        href = name_pep['href']
        pep_link = urljoin(PEPS_DOC_URL, href)
        response1 = session.get(pep_link)
        response1.encoding = 'utf-8'
        soup = BeautifulSoup(response1.text, 'lxml')
        in_card_pep_name = soup.find('title').text.split(' – ')[0]
        # Спарсенное наименование PEP внутри карточки

        status_in_card_pep = soup.find('abbr').text  # Спарсенный статус
        # внутри PEP

        in_card_statuses.append(status_in_card_pep)

        compare_statuses_dict = {status_pep_general: status_in_card_pep}
        compare_list_statuses.append(compare_statuses_dict)

    status_count = Counter(in_card_statuses)
    table = PrettyTable()
    table.field_names = ['Статус', 'Количество']
    for status, count in sorted(status_count.items()):
        table.add_row([status, count])
    table.add_row(['----------', '----------'])
    table.add_row(['Total', sum(status_count.values())])
    print(table)
    compare_statuses(compare_list_statuses)
