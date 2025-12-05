class User:
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        if isinstance(value, int) and value > 0:
            self.__id = value
        else:
            raise ValueError("id пользователя должен быть положительным целым числом")

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if isinstance(value, str) and len(value) >= 2:
            self.__name = value
        else:
            raise ValueError("Некорректное имя пользователя")
