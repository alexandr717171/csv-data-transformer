from app.running_scripts.argparse_script import parser_arguments, parser
from app.services.csv_file_reading import AverageGDP
from config import PATH_FOLDER

# Реестр доступных отчетов: сопоставляем строку из терминала с классом
REPORTS = {
    'average_gdp': AverageGDP,
    # Сюда просто добавляйте новые отчеты, например: 'inflation': InflationReport,
}


def main():
    """
    Основная логика запуска: считывает аргументы, выбирает
    нужный класс по значению аргумента --report и выводит результат в консоль,
    используя метод родительского класса Processing - tabulate.
    """
    # Извлекаем пути к файлам (files) и тип отчета (report_type)
    files, report_type = parser_arguments(parser)
    if files is None:
        print('Введите пути к файлам: --files example.file')
        return
    for filename in files:
        path_file = PATH_FOLDER / filename
        if not path_file.exists():
            print(f'Такого файла нет: {path_file}')
            return

    # Проверка: существует ли запрошенный тип отчета в нашем реестре
    if report_type in REPORTS:
        # Инициализируем класс (например, AverageGDP)
        report_class = REPORTS[report_type]
        processing_instance = report_class(file_name_list=files)

        # Генерируем и печатаем таблицу
        processing_instance.tabulate()
    else:
        print(f"Ошибка: Аргумент --report '{report_type}' не распознан.")


if __name__ == '__main__':
    main()