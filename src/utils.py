import logging

from bs4 import BeautifulSoup

from exceptions import ParserFindTagException, ParserGetResponseException
from constants import DEFAULT_ENCODING


def get_response(session, url, encoding=DEFAULT_ENCODING):
    """ Метод получения ответа от сервера """
    response = session.get(url)
    response.encoding = encoding
    if not response:
        error_msg = f'Не удалось загрузить страницу {url}'
        logging.error(error_msg, stack_info=True)
        raise ParserGetResponseException(error_msg)
    return response


def find_tag(soup, tag, attrs=None):
    """ Метод поиска тега """
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def get_soup(session, url, features):
    """ Метод получения супа """
    response = get_response(session, url)
    soup = BeautifulSoup(response.text, features=features)
    return soup
