import requests_cache
from bs4 import BeautifulSoup

from constants import MAIN_DOC_URL

session = requests_cache.CachedSession()
response = session.get(MAIN_DOC_URL)
response.encoding = 'utf-8'
soup = BeautifulSoup(response.text, 'lxml')

num_index_section = soup.find('section', attrs={'id': 'numerical-index'})
peps_body_table = num_index_section.find('tbody')
peps_a = peps_body_table.find_all('tr')
count = 0
for pep_a in peps_a:
    name_pep = pep_a.find('a')
    print(name_pep)
    count += 1
print(count)
