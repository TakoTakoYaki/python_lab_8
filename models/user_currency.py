class UserCurrency:
    """
    Таблица-связка: многие-ко-многим между User и Currency.
    """

    def __init__(self, id: int, user_id: int, currency_id: int):
        self.id = id
        self.user_id = user_id
        self.currency_id = currency_id

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int):
        if isinstance(value, int) and value > 0:
            self.__id = value
        else:
            raise ValueError("id связи должен быть положительным целым числом")

    @property
    def user_id(self) -> int:
        return self.__user_id

    @user_id.setter
    def user_id(self, value: int):
        if isinstance(value, int) and value > 0:
            self.__user_id = value
        else:
            raise ValueError("user_id должен быть положительным целым числом")

    @property
    def currency_id(self) -> int:
        return self.__currency_id

    @currency_id.setter
    def currency_id(self, value: int):
        if isinstance(value, int) and value > 0:
            self.__currency_id = value
        else:
            raise ValueError("currency_id должен быть положительным целым числом")
