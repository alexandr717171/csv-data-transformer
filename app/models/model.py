"""
Модуль базовых структур данных и моделей трансформации.

Предоставляет унифицированные классы (DTO) для хранения, валидации
и первичной обработки данных.

Классы в этом модуле предназначены для обработки данных и обеспечивают
типизацию на этапе инициализации объектов.
"""

from dataclasses import dataclass



@dataclass
class Base:
    """
    Класс-контейнер для хранения макроэкономических данных страны.

    Выполняет автоматическое преобразование типов для всех числовых атрибутов
    в методе __post_init__.

    Attributes:
        country (str): Название страны.
        year (int): Год наблюдения.
        gdp (int): ВВП (номинал или по ППС).
        gdp_grow (float): Рост ВВП в процентах.
        inflation (float): Уровень инфляции.
        unemployment (float): Уровень безработицы.
        population (int): Численность населения.
        continent (str): Континент.
    """
    country: str
    year: int
    gdp: int
    gdp_grow: float
    inflation: float
    unemployment: float
    population: int
    continent: str

    def __post_init__(self):
        self.year = int(self.year)
        self.gdp = int(self.gdp)
        self.gdp_grow = float(self.gdp_grow)
        self.inflation = float(self.inflation)
        self.unemployment = float(self.unemployment)
        self.population = int(self.population)
