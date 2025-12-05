class Author:
    def __init__(self, name: str, group: str):
        self.name = name
        self.group = group

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if isinstance(value, str) and len(value) >= 2:
            self.__name = value
        else:
            raise ValueError("Ошибка при задании имени автора")

    @property
    def group(self) -> str:
        return self.__group

    @group.setter
    def group(self, value: str):
        if isinstance(value, str) and len(value) >= 3:
            self.__group = value
        else:
            raise ValueError("Ошибка при задании группы автора")
