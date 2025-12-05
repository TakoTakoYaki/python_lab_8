from .author import Author


class App:
    def __init__(self, name: str, version: str, author: Author):
        self.name = name
        self.version = version
        self.author = author

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str):
        if isinstance(value, str) and value:
            self.__name = value
        else:
            raise ValueError("Некорректное имя приложения")

    @property
    def version(self) -> str:
        return self.__version

    @version.setter
    def version(self, value: str):
        if isinstance(value, str) and value:
            self.__version = value
        else:
            raise ValueError("Некорректная версия приложения")

    @property
    def author(self) -> Author:
        return self.__author

    @author.setter
    def author(self, value: Author):
        from .author import Author
        if isinstance(value, Author):
            self.__author = value
        else:
            raise TypeError("author должен быть экземпляром класса Author")
