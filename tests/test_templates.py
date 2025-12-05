import unittest
from jinja2 import Environment, PackageLoader, select_autoescape

from models import Author, App, User, Currency


class TestTemplates(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.env = Environment(
            loader=PackageLoader("myapp"),
            autoescape=select_autoescape()
        )

    def test_index_template_context(self):
        template = self.env.get_template("index.html")
        author = Author("Иван", "P3120")
        app = App("CurrenciesListApp", "1.0.0", author)

        html = template.render(
            app=app,
            navigation=[{"caption": "Главная", "href": "/"}],
        )

        self.assertIn("CurrenciesListApp", html)
        self.assertIn("Иван", html)
        self.assertIn("P3120", html)
        self.assertIn("Главная", html)
        self.assertIn('href="/"', html)

    def test_users_template_loop(self):
        template = self.env.get_template("users.html")
        author = Author("Иван", "P3120")
        app = App("CurrenciesListApp", "1.0.0", author)

        users = [User(1, "Алиса"), User(2, "Боб")]

        html = template.render(app=app, users=users)
        self.assertIn("Пользователи", html)
        self.assertIn("Алиса", html)
        self.assertIn("Боб", html)
        self.assertIn("/user?id=1", html)
        self.assertIn("/user?id=2", html)

    def test_currencies_template_loop(self):
        template = self.env.get_template("currencies.html")
        author = Author("Иван", "P3120")
        app = App("CurrenciesListApp", "1.0.0", author)

        currencies = [
            Currency(id=1, num_code=840, char_code="USD", name="Доллар США", value=90.5, nominal=1),
            Currency(id=2, num_code=978, char_code="EUR", name="Евро", value=100.7, nominal=1),
        ]

        html = template.render(app=app, currencies=currencies)
        self.assertIn("Курсы валют", html)
        self.assertIn("USD", html)
        self.assertIn("EUR", html)
        self.assertIn("Доллар США", html)
        self.assertIn("Евро", html)


if __name__ == "__main__":
    unittest.main()
