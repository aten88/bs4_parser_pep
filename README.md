Парсер документации Python/PEP

# Описание:
Программа - парсер [документации Python](https://peps.python.org/) которая имеет 4 режима работы:
1. `whats-new` - ищет ссылки на статьи о нововведениях в Python, переходит по ним и собирает информацию об авторах и редакторах статей.
2. `latest-versions` - собирает информацию обо всех статусах версий Python;
3. `download` - скачивает архив с актуальной документацией Python в формате .zip;
4. `pep` - считает количество PEP-документов в каждом статусе и общее количество PEP, сравнивая при этом статус на странице PEP со статусом в общем списке.

Вывод результатов реализован в 3 видах на выбор пользователя:
- построчный вывод в консоль;
- вывод в консоль таблицей;
- сохранение в файл формата csv;

# Технологии
[![Python](https://img.shields.io/badge/Python-3.9-3776AB?logo=python)](https://www.python.org/)
[![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-4.9-3776AB)](https://www.crummy.com/software/BeautifulSoup/)
[![Requests](https://img.shields.io/badge/Requests-2.27-3776AB)](https://requests.readthedocs.io/)
[![Prettytable](https://ptable.readthedocs.io/en/latest/tutorial.html)]

# Запуск проекта
Клонировать репозиторий и перейти в директорию проекта:
-git clone https://github.com/aten88/bs4_parser_pep
-cd bs4_parser_pep

Cоздать и активировать виртуальное окружение:
-python -m venv venv
-source venv/Scripts/activate

Обновить пакетный менеджер PIP и установить зависимости из файла requirements.txt:
-python -m pip install --upgrade pip
-pip install -r requirements.txt

Перейти в директорию с файлом main.py
-cd src

Ознакомиться со справкой и/или запустить проект в нужном режиме:
-python main.py --help
-python main.py [-h] [-c] [-o {pretty,file}] {whats-new, latest-versions, download, pep}