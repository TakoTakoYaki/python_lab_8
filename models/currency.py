class Currency:
    def __init__(
        self,
        id: int | None,
        num_code: int | None,
        char_code: str,
        name: str | None,
        value: float,
        nominal: int = 1,
    ):
        self.id = id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def id(self) -> int | None:
        return self.__id

    @id.setter
    def id(self, value: int | None):
        if value is None or (isinstance(value, int) and value > 0):
            self.__id = value
        else:
            raise ValueError("id валюты должен быть положительным int или None")

    @property
    def num_code(self) -> int | None:
        return self.__num_code

    @num_code.setter
    def num_code(self, value: int | None):
        if value is None or (isinstance(value, int) and value > 0):
            self.__num_code = value
        else:
            raise ValueError("num_code должен быть положительным int или None")

    @property
    def char_code(self) -> str:
        return self.__char_code

    @char_code.setter
    def char_code(self, value: str):
        if isinstance(value, str) and len(value) in (3, 4):
            self.__char_code = value
        else:
            raise ValueError("char_code должен быть строкой из 3–4 символов")

    @property
    def name(self) -> str | None:
        return self.__name

    @name.setter
    def name(self, value: str | None):
        if value is None or (isinstance(value, str) and value):
            self.__name = value
        else:
            raise ValueError("Некорректное название валюты")

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: float):
        if isinstance(value, (int, float)) and value >= 0:
            self.__value = float(value)
        else:
            raise ValueError("Курс валюты должен быть неотрицательным числом")

    @property
    def nominal(self) -> int:
        return self.__nominal

    @nominal.setter
    def nominal(self, value: int):
        if isinstance(value, int) and value > 0:
            self.__nominal = value
        else:
            raise ValueError("Номинал должен быть положительным целым числом")
