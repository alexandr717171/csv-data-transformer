"""
Модуль конфигурации pytest.

Содержит общие фикстуры для создания тестового окружения, включая
генерацию временных CSV-файлов и расчет эталонных (ожидаемых) данных.
"""


import csv
from collections import defaultdict

import pytest

# Тестовые данные для генерации файлов
data_csv_file_1 = [
    ('country', 'year', 'gdp', 'gdp_growth', 'inflation', 'unemployment', 'population', 'continent'),
    ('United States', '2023', '25462', '2.1', '3.4', '3.7', '339', 'North America'),
    ('United States', '2022', '23315', '2.1', '8.0', '3.6', '338', 'North America'),
    ('Japan', '2023', '4230', '1.9', '3.2', '2.4', '125', 'Asia'),
    ('Japan', '2022', '4235', '1.0', '2.5', '2.6', '125', 'Asia'),
]

data_csv_file_2 = [
    ('country', 'year', 'gdp', 'gdp_growth', 'inflation', 'unemployment', 'population', 'continent'),
    ('Mexico', '2023', '1414', '3.2', '4.7', '2.9', '128', 'North America'),
    ('Mexico', '2022', '1274', '3.9', '7.9', '3.3', '127', 'North America'),

]



@pytest.fixture
def sample_data_file(tmp_path):
    """
    Фикстура для создания временных CSV-файлов.

    Args:
        tmp_path: Встроенная фикстура pytest для создания временной директории.
    Returns:
        tuple: Пути (Path) к двум созданным файлам.
    """
    file_path_1 = tmp_path / 'data_test_1.csv'
    file_path_2 = tmp_path / 'data_test_2.csv'
    with open(file_path_1, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data_csv_file_1)

    with open(file_path_2, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(data_csv_file_2)
    return file_path_1, file_path_2

@pytest.fixture
def expected_data_one_file():
    """
    Функция для создания списка средних значений ввп отсортированного для данных имитирующих один файл.
    :return: list
    """
    dict_average_gdb =defaultdict(list)
    for line in data_csv_file_1[1:]:
        dict_average_gdb[line[0]].append(float(line[2]))
    list_average_gdb = []
    for key in dict_average_gdb:
        list_average_gdb.append((key, sum(dict_average_gdb[key]) / len(dict_average_gdb[key])))
    list_average_gdb.sort(key=lambda x: x[1], reverse=True)
    return list_average_gdb

@pytest.fixture
def expected_data_two_file():
    """
    Функция для создания списка средних значений ввп отсортированного для данных имитирующих два файла.
    :return: list
    """
    dict_average_gdb =defaultdict(list)
    data_csv_file_1.extend(data_csv_file_2[1:])
    for line in data_csv_file_1[1:]:
        dict_average_gdb[line[0]].append(float(line[2]))
    list_average_gdb = []
    for key in dict_average_gdb:
        list_average_gdb.append((key, sum(dict_average_gdb[key]) / len(dict_average_gdb[key])))
    list_average_gdb.sort(key=lambda x: x[1], reverse=True)
    return list_average_gdb





