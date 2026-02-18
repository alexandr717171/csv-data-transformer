"""
Модуль интеграционного тестирования CLI-интерфейса.

Проверяет корректность работы приложения при запуске через subprocess,
сравнивая реальный вывод в консоль с эталонными данными и таблицами tabulate.
"""

import subprocess

from tabulate import tabulate

from config import PATH_FOLDER

# Заголовки для генерации эталонных таблиц в тестах
headers = ['country', 'gdp']


def test_one_file(sample_data_file, expected_data_one_file):
    """Тест обработки одного корректного CSV файла."""
    data = subprocess.run(['python', 'main.py', '--files', sample_data_file[0], '--report', 'average_gdp'],
                          capture_output=True,
                          text=True)
    data_rstrip = data.stdout.rstrip()

    # Генерируем ожидаемую таблицу программно для сравнения
    expected = tabulate(expected_data_one_file, headers=headers, tablefmt='grid', floatfmt=".2f",
                        showindex=range(1, len(expected_data_one_file) + 1))
    assert data_rstrip == expected


def test_two_files(sample_data_file, expected_data_two_file):
    """Тест агрегации данных из двух CSV файлов одновременно."""
    data = subprocess.run(['python', 'main.py', '--files', sample_data_file[0], sample_data_file[1],
                           '--report', 'average_gdp'], capture_output=True, text=True)
    data_rstrip = data.stdout.rstrip()
    expected = tabulate(expected_data_two_file, headers=headers, tablefmt='grid', floatfmt=".2f",
                        showindex=range(1, len(expected_data_two_file) + 1))
    assert data_rstrip == expected

def test_required_file():
    """Проверка ошибки при отсутствии обязательного аргумента --files."""
    data = subprocess.run(['python', 'main.py', '--report', 'average_gdp'],
                          capture_output=True,
                          text=True)
    data_rstrip = data.stdout.rstrip()
    assert data_rstrip == 'Введите пути к файлам: --files example.file'

def test_wrong_path_to_file(sample_data_file, expected_data_one_file):
    """Проверка вывода при указании несуществующего пути к файлу."""
    data = subprocess.run(['python', 'main.py', '--files', 'wrong_path', '--report', 'average_gdp'],
                          capture_output=True,
                          text=True)
    path_file = PATH_FOLDER / 'wrong_path'
    data_rstrip = data.stdout.rstrip()
    expected = f'Такого файла нет: {path_file}'
    assert data_rstrip == expected


def test_required_report(sample_data_file):
    """Проверка стандартной ошибки argparse при отсутствии флага --report (проверяется stderr)."""
    data = subprocess.run(['python', 'main.py', '--files', sample_data_file[0], sample_data_file[1]],
                          capture_output=True, text=True)
    data_error = data.stderr.rstrip()
    expected_text = ' error: the following arguments are required: --report'
    assert expected_text in data_error


def test_required_argument_for_report(sample_data_file):
    """Проверка стандартной ошибки argparse при отсутствии аргументов для  флага --report (проверяется stderr)."""
    data = subprocess.run(['python', 'main.py', '--files', sample_data_file[0],
                           sample_data_file[1], '--report'],
                          capture_output=True, text=True)
    data_error = data.stderr.rstrip()
    expected_text = 'error: argument --report: expected one argument'
    assert expected_text in data_error


def test_incorrect_argument_for_report(sample_data_file):
    """Проверка кастомной ошибки при передаче неизвестного типа отчета."""
    data = subprocess.run(['python', 'main.py', '--file', sample_data_file[0],
                           sample_data_file[1], '--report', 'wrong_argument'],
                          capture_output=True, text=True)
    data_rstrip = data.stdout.rstrip()
    report_type = 'wrong_argument'
    expected_text = f"Ошибка: Аргумент --report '{report_type}' не распознан."
    f"- Ошибка: Аргумент --report '{report_type}' не распознан."
    assert data_rstrip == expected_text
