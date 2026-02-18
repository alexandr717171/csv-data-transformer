"""
Модуль обработки аргументов командной строки.

Отвечает за определение путей к файлам и выбор типа отчета при запуске
скрипта через терминал.
"""

import argparse

parser = argparse.ArgumentParser(description='executing operations with csv files')

def parser_arguments(parser_obj: argparse.ArgumentParser) -> tuple[list[str], str]:
    """
    Конфигурирует и считывает аргументы командной строки.

    Args:
        parser_obj (argparse.ArgumentParser): Объект парсера для настройки.

    Returns:
        tuple[list[str], str]: Кортеж, содержащий:
            - список путей к CSV-файлам (args_files)
            - тип формируемого отчета (args_report)
    """

    parser_obj.add_argument(
        '--files',
        nargs='+',
        help='Пути к одному или нескольким CSV-файлам для обработки'
    )
    parser_obj.add_argument(
        '--report',
        help='Тип операции или вид отчета',
        required=True
    )
    args = parser_obj.parse_args()
    args_files = args.files
    args_report = args.report
    return args_files, args_report




