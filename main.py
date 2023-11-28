from urllib.parse import urljoin
import requests_cache
from bs4 import BeautifulSoup

from constants import PEPS_DOC_URL

session = requests_cache.CachedSession()
response = session.get(PEPS_DOC_URL)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

num_index_section = soup.find('section', attrs={'id': 'numerical-index'})
peps_body_table = num_index_section.find('tbody')
peps_tr = peps_body_table.find_all('tr')

count_peps_doc = 0  # Счетчик кол-ва PEP

exterior_list_pep = []
interior_list_pep = []

for pep_a in peps_tr:
    name_pep = pep_a.find('a')
    title_name_general = name_pep['title']  # Название PEP из внешней таблицы

    td_pep = pep_a.find('td')
    abbr_pep = td_pep.find('abbr')
    status_pep_general = abbr_pep['title'].split(", ", 1)[1]
    # Статус PEP из общей таблицы

    dict_pep_ext = {status_pep_general: title_name_general}
    exterior_list_pep.append(dict_pep_ext)

    href = name_pep['href']
    pep_link = urljoin(PEPS_DOC_URL, href)
    count_peps_doc += 1
    response1 = session.get(pep_link)
    response1.encoding = 'utf-8'
    soup = BeautifulSoup(response1.text, 'lxml')
    in_card_pep_name = soup.find('title').text.replace(
        " | peps.python.org", ""
    )  # Спарсенное наименование PEP внутри карточки

    status_in_card_pep = soup.find('abbr').text  # Спарсенный статус внутри PEP

    if status_pep_general != status_in_card_pep:
        print('Найдено отличие. ')
    dict_pep_int = {status_in_card_pep: in_card_pep_name}
    interior_list_pep.append(dict_pep_int)
print(exterior_list_pep)
print(interior_list_pep)
