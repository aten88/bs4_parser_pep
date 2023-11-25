import requests
from bs4 import BeautifulSoup

from constants import MAIN_DOC_URL


response = requests.get(MAIN_DOC_URL)
soup = BeautifulSoup(response.text, 'lxml')
print(soup)
