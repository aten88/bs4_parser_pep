import csv

from constants import BASE_DIR


def file_outputs(data, total):
    results_dir = BASE_DIR / 'results'
    results_dir.mkdir(exist_ok=True)
    file_name = results_dir / 'status_table.csv'
    with open(file_name, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, dialect='unix')
        writer.writerow(['Статус', 'Количество'])
        for status, count in data.items():
            writer.writerow([status, count])
        writer.writerow(['Total', total])
