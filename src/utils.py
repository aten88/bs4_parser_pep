import logging

from requests import RequestException

from exceptions import ParserFindTagException
from constants import EXPECTED_STATUS
from configs import configure_logging


def get_response(session, url):
    """Метод получения ответа от сервера. """
    try:
        response = session.get(url)
        response.encoding = 'utf-8'
        return response
    except RequestException:
        logging.exception(
            f'Возникла ошибка при загрузке страницы: {url}',
            stack_info=True
        )


def find_tag(soup, tag, attrs=None):
    """Метод поиска тега. """
    searched_tag = soup.find(tag, attrs=(attrs or {}))
    if searched_tag is None:
        error_msg = f'Не найден тег {tag} {attrs}'
        logging.error(error_msg, stack_info=True)
        raise ParserFindTagException(error_msg)
    return searched_tag


def compare_statuses(combined_list_with_links):
    """ Метод проверки соответствия статусов PEP. """
    configure_logging()
    updated_list = []
    for item in combined_list_with_links:
        key, value = list(item.items())[0]
        pep_link = value['pep_link']
        status_pep_general = key
        status_in_card_pep = value['status_in_card']

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
            updated_list.append(status_in_card_pep)
        else:
            logging.error(
                f'\n'
                f'Несовпадающие статусы:\n'
                f'{pep_link}\n'
                f'Статус в карточке: {status_in_card_pep}\n'
                f'Ожидаемые статусы: {expected_status}\n'
            )
    return updated_list
