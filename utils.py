import logging

from constants import EXPECTED_STATUS
from configs import configure_logging


def compare_statuses(combined_list):
    """ Метод проверки соответствия статусов PEP. """
    configure_logging()
    updated_list = []
    for item in combined_list:
        key, value = list(item.items())[0]

        expected_status = EXPECTED_STATUS.get(key)
        if expected_status is None:
            logging.error(
                f'\n'
                f'Статус в карточке: {key}'
                f'Ожидаемые статусы: {value}'
            )
            continue
        if value in expected_status:
            updated_list.append(value)
        else:
            logging.error(
                f'\n'
                f'Несовпадающие статусы:\n'
                f'Статус в карточке: {value}\n'
                f'Ожидаемые статусы: {expected_status}'
            )
    return updated_list
