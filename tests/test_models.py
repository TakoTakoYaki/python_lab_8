import unittest

from models import Author, App, User, Currency, UserCurrency


class TestAuthorModel(unittest.TestCase):
    def test_author_getters_setters_ok(self):
        a = Author("Иван", "P3120")
        self.assertEqual(a.name, "Иван")
        self.assertEqual(a.group, "P3120")

        a.name = "Пётр"
        a.group = "P3221"
        self.assertEqual(a.name, "Пётр")
        self.assertEqual(a.group, "P3221")

    def test_author_invalid_name(self):
        with self.assertRaises(ValueError):
            Author("", "P3120")

    def test_author_invalid_group(self):
        with self.assertRaises(ValueError):
            Author("Иван", "")


class TestUserModel(unittest.TestCase):
    def test_user_ok(self):
        u = User(1, "Алиса")
        self.assertEqual(u.id, 1)
        self.assertEqual(u.name, "Алиса")

    def test_user_invalid_id(self):
        with self.assertRaises(ValueError):
            User(0, "Алиса")

    def test_user_invalid_name(self):
        with self.assertRaises(ValueError):
            User(1, "A")


class TestCurrencyModel(unittest.TestCase):
    def test_currency_ok(self):
        c = Currency(
            id=1,
            num_code=840,
            char_code="USD",
            name="Доллар США",
            value=90.5,
            nominal=1,
        )
        self.assertEqual(c.char_code, "USD")
        self.assertEqual(c.value, 90.5)
        self.assertEqual(c.nominal, 1)

    def test_currency_negative_value(self):
        with self.assertRaises(ValueError):
            Currency(
                id=1,
                num_code=840,
                char_code="USD",
                name="Доллар США",
                value=-1.0,
                nominal=1,
            )

    def test_currency_invalid_nominal(self):
        c = Currency(
            id=1,
            num_code=840,
            char_code="USD",
            name="Доллар США",
            value=90.5,
            nominal=1,
        )
        with self.assertRaises(ValueError):
            c.nominal = 0


class TestUserCurrencyModel(unittest.TestCase):
    def test_user_currency_ok(self):
        uc = UserCurrency(1, user_id=1, currency_id=2)
        self.assertEqual(uc.id, 1)
        self.assertEqual(uc.user_id, 1)
        self.assertEqual(uc.currency_id, 2)

    def test_user_currency_invalid_ids(self):
        with self.assertRaises(ValueError):
            UserCurrency(0, user_id=1, currency_id=2)
        with self.assertRaises(ValueError):
            UserCurrency(1, user_id=0, currency_id=2)
        with self.assertRaises(ValueError):
            UserCurrency(1, user_id=1, currency_id=0)


if __name__ == "__main__":
    unittest.main()
