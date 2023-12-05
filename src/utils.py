import logging

from requests import RequestException
from bs4 import BeautifulSoup

from exceptions import ParserFindTagException
from constants import DEFAULT_ENCODING


def get_response(session, url, encoding=DEFAULT_ENCODING):
    """ Метод получения ответа от сервера """
    try:
        response = session.get(url)
        response.encoding = encoding
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы: {url}',
            stack_info=True
        )


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
    if response is None:
        return
    soup = BeautifulSoup(response.text, features=features)
    return soup
