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
count = 0
for pep_a in peps_a:
    name_pep = pep_a.find('a')
    href = name_pep['href']
    pep_link = urljoin(PEPS_DOC_URL, href)
    print(pep_link)
    count += 1
print(count)
