from constants import EXPECTED_STATUS


def compare_statuses(combined_list):
    """ Метод проверки соответствия статусов PEP"""
    for item in combined_list:
        key, value = list(item.items())[0]

        expected_status = EXPECTED_STATUS.get(key)
        if expected_status is None:
            print(f"Ошибка: Неожиданный статус '{key}' для '{value}' в списке")
            continue

        if value not in expected_status:
            print(
                f"Ошибка: Несоответствие статуса для '{value}'. "
                f"Ожидалось: {expected_status}, получено: '{value}'"
            )
