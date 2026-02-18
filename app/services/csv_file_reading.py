"""
Модуль обработки данных и генерации отчетов.

Содержит механизмы для чтения CSV-файлов, агрегации данных в словари
и визуализации результатов в виде таблиц. Использует абстрактные классы
для реализации различных стратегий анализа данных (например, расчет среднего ВВП).
"""
import csv
from abc import ABC, abstractmethod
from collections import defaultdict
from pathlib import Path

from tabulate import tabulate

from app.models.model import Base
from config import BASE_DIR, PATH_FOLDER


class CreateBasedDictionary:
    """
    Класс для чтения CSV и первичной группировки данных по странам.
    """
    def __init__(self, file_name_list: list[str], path_folder: Path = PATH_FOLDER):
        self.file_name_list = file_name_list
        self.path_folder = path_folder
        self.list_files = []
        self.country_dict = defaultdict(list)


    def path_to_files(self):
        """Превращает список имен файлов в список полных путей Path."""

        for filename in self.file_name_list:
            self.list_files.append(PATH_FOLDER / filename)



    def csv_file_reader(self, filename: Path):
        """
        Считывает один CSV файл и преобразует строки в объекты Base.
        Данные группируются в self.country_dict.
        Для трансформации данных используется класс Base из модуля models.
        """

        with open(filename, encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_reader.__next__()
            for row in csv_reader:
                base = Base(*row)
                # self.country_dict = defaultdict(list) общий словарь для разных файлов из def __init__
                self.country_dict[base.country].append([base.year,
                                                  base.gdp,
                                                  base.gdp_grow,
                                                  base.inflation,
                                                  base.unemployment,
                                                  base.population,
                                                  base.continent
                                                  ])

    def csv_file_reader_all_files(self):
        """
        Запускает последовательное чтение всех файлов из списка.
        За счет того, что используется один словарь для записи в классе
        self.country_dict данные группируются независимо от количества файлов.
        self.country_dict - собирает данные со всех файлов.
        """
        self.path_to_files()
        for filename in self.list_files:
            self.csv_file_reader(filename)


class ProcessingMethod(CreateBasedDictionary, ABC):
    """
    Абстрактный класс для методов обработки.
    Определяет интерфейс создания отчета и вывода его в консоль.

      ИНСТРУКЦИЯ ПО ДОБАВЛЕНИЮ НОВОГО ОТЧЕТА:
    1. Создайте новый класс, наследуясь от `ProcessingMethod`.
    2. В методе `__init__` переопределите `self.headers` (список названий столбцов).
    3. Реализуйте метод `method_for_data`, который должен возвращать
       отсортированный список кортежей/списков для отрисовки в таблице.

    Пример:
        class MyNewReport(ProcessingMethod):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.headers = ['Заголовок 1', 'Заголовок 2']

            def method_for_data(self):
                # Ваша логика обработки self.country_dict
                return [('Данные 1', 100), ('Данные 2', 200)]
    """
    def __init__(self, file_name_list: list[str], path_folder: Path = PATH_FOLDER):
        super().__init__(file_name_list, path_folder)
        self.csv_file_reader_all_files()
        self.method_for_data()
        self.headers = []

    @abstractmethod
    def method_for_data(self):
        """
        Абстрактный метод для реализации логики конкретного отчета.
        Должен возвращать список кортежей с данными.
        """
        pass

    def tabulate(self):
        """Выводит данные отчета в виде форматированной таблицы в консоль."""
        list_sorted = self.method_for_data()
        data = tabulate(list_sorted, headers=self.headers, tablefmt="grid", floatfmt=".2f", showindex=range(1, len(list_sorted) + 1))
        print(data)

class AverageGDP(ProcessingMethod):
    """
    Реализация отчета: Средний показатель ВВП по странам.
    Сортирует данные от большего к меньшему.
    """
    def __init__(self, file_name_list: list[str], path_folder: Path = PATH_FOLDER):
        super().__init__(file_name_list, path_folder)
        self.headers = ['country', 'gdp']


    def method_for_data(self) -> list[tuple]:
        """Расчитывает среднее значение ВВП для каждой страны."""
        dict_average_gdp = dict()
        for key, value in self.country_dict.items():
            # item_list[1] соответствует индексу ВВП в структуре данных
            dict_average_gdp[key] = round(sum(item_list[1] for item_list in value) / len(value), 2)
        # Сортировка по убыванию среднего ВВП
        list_sorted = sorted(dict_average_gdp.items(), key=lambda x: x[1], reverse=True)
        return list_sorted




