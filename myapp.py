from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from jinja2 import Environment, PackageLoader, select_autoescape

from models import Author, App, User, Currency, UserCurrency
from utils.currencies_api import get_currencies



# Инициализация моделей
main_author = Author("Николай Бадмаев", "P4150")
app_info = App("CurrenciesListApp", "1.0.0", main_author)

# Простая база
USERS: list[User] = [
    User(1, "Алиса"),
    User(2, "Боб"),
]

# База валют
CURRENCIES: list[Currency] = [
    Currency(id=1, num_code=None, char_code="USD", name="Доллар США", value=0.0, nominal=1),
    Currency(id=2, num_code=None, char_code="EUR", name="Евро", value=0.0, nominal=1),
    Currency(id=3, num_code=None, char_code="GBP", name="Фунт стерлингов", value=0.0, nominal=1),
]

# Подписки: Алиса на USD и EUR, Боб - только на GBP
USER_CURRENCIES: list[UserCurrency] = [
    UserCurrency(1, user_id=1, currency_id=1),
    UserCurrency(2, user_id=1, currency_id=2),
    UserCurrency(3, user_id=2, currency_id=3),
]


# Jinja2
env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_user = env.get_template("user.html")
template_currencies = env.get_template("currencies.html")


def find_user(user_id: int) -> User | None:
    for u in USERS:
        if u.id == user_id:
            return u
    return None


def find_currency_by_id(currency_id: int) -> Currency | None:
    for c in CURRENCIES:
        if c.id == currency_id:
            return c
    return None


def update_currency_rates() -> None:
    """Обновляем курсы валют через get_currencies."""
    codes = [c.char_code for c in CURRENCIES]
    data = get_currencies(codes)
    for c in CURRENCIES:
        if c.char_code in data:
            c.value = data[c.char_code]


class MyRequestHandler(BaseHTTPRequestHandler):
    def _send_html(self, html: str, status: int = 200):
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/":
            # главная страница
            nav = [
                {"caption": "Главная", "href": "/"},
                {"caption": "Пользователи", "href": "/users"},
                {"caption": "Валюты", "href": "/currencies"},
                {"caption": "Об авторе", "href": "/author"},
            ]
            html = template_index.render(app=app_info, navigation=nav)

            self._send_html(html)

        elif path == "/users":
            html = template_users.render(app=app_info, users=USERS)
            self._send_html(html)

        elif path == "/user":
            # /user?id=1
            if "id" not in params:
                self._send_html("<h1>Missing id</h1>", status=400)
                return

            try:
                user_id = int(params["id"][0])
            except ValueError:
                self._send_html("<h1>Invalid id</h1>", status=400)
                return

            user = find_user(user_id)
            if user is None:
                self._send_html("<h1>User not found</h1>", status=404)
                return

            # находим подписки и соответствующие валюты
            user_cur_ids = [
                uc.currency_id
                for uc in USER_CURRENCIES
                if uc.user_id == user.id
            ]
            currencies = [
                c for c in CURRENCIES if c.id in user_cur_ids
            ]

            html = template_user.render(app=app_info, user=user, currencies=currencies)
            self._send_html(html)

        elif path == "/currencies":
            # обновляем курсы при каждом заходе
            try:
                update_currency_rates()
                html = template_currencies.render(app=app_info, currencies=CURRENCIES)
                self._send_html(html)
            except Exception as e:
                self._send_html(f"<h1>Error updating currencies: {e}</h1>", status=500)

        elif path == "/author":
            # можно просто отрендерить index, но в простом виде:
            html = f"""
            <html><body>
            <h1>Об авторе</h1>
            <p>Имя: {main_author.name}</p>
            <p>Группа: {main_author.group}</p>
            <p><a href="/">На главную</a></p>
            </body></html>
            """
            self._send_html(html)

        else:
            self._send_html("<h1>404 Not Found</h1>", status=404)


def run_server(host: str = "localhost", port: int = 8080):
    httpd = HTTPServer((host, port), MyRequestHandler)
    print(f"Server is running on http://{host}:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run_server()
