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
peps_a = peps_body_table.find_all('tr')
# print(peps_a)
count_peps_doc = 0  # Счетчик кол-ва PEP
for pep_a in peps_a:
    name_pep = pep_a.find('a')
    td_pep = pep_a.find('td')
    abbr_pep = td_pep.find('abbr')
    status_pep_general = abbr_pep['title'].split(", ", 1)[1]
    # Статус PEP из общей таблицы
    title_name_general = name_pep['title']  # Название PEP из внешней таблицы
    print(f'{status_pep_general} | во внешней таблице')
    href = name_pep['href']
    pep_link = urljoin(PEPS_DOC_URL, href)
    count_peps_doc += 1
    response = session.get(pep_link)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'lxml')
    in_card_pep_name = soup.find('title').text.replace(
        " | peps.python.org", ""
    )  # Спарсенное наименование PEP внутри карточки
    status_in_card_pep = soup.find('abbr').text  # Спарсенный статус внутри PEP
    print(f'{status_in_card_pep} | внутри карточки')
    no_match = 0
    if status_pep_general != status_in_card_pep:
        no_match += 1
        print('Найдено отличие. ')
    print('---------------------------------------------------------------')

print('----------------------------')
print(count_peps_doc)
print(no_match)
