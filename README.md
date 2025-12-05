# Отчёт по лабораторной работе  
**Тема:** Простое клиент-серверное приложение на Python (HTTPServer + Jinja2 + MVC)

---

## 1. Цель работы

Цель работы - разработать простое клиент-серверное веб-приложение на Python **без серверных фреймворков**, используя:

- `HTTPServer` и `BaseHTTPRequestHandler` для обработки HTTP-запросов и маршрутизации;
- шаблонизатор **Jinja2** для формирования HTML-страниц;
- собственные **модели** предметной области (Author, App, User, Currency, UserCurrency) с геттерами и сеттерами;
- функцию `get_currencies` для получения актуальных курсов валют с внешнего API;
- простую архитектуру в стиле **MVC**;
- модуль `unittest` для тестирования моделей, контроллера и работы с API.

---

## 2. Описание предметной области

В приложении используются следующие модели:

- **Author**
  - `name` - имя автора;
  - `group` - учебная группа.
- **App**
  - `name` - название приложения;
  - `version` - версия;
  - `author` - объект `Author`.
- **User**
  - `id` - уникальный идентификатор пользователя;
  - `name` - имя пользователя.
- **Currency**
  - `id` - уникальный идентификатор;
  - `num_code` - цифровой код валюты;
  - `char_code` - символьный код (например, `USD`, `EUR`);
  - `name` - название валюты;
  - `value` - текущий курс;
  - `nominal` - за сколько единиц валюты указан курс.
- **UserCurrency**
  - `id` - идентификатор записи;
  - `user_id` - внешний ключ к `User`;
  - `currency_id` - внешний ключ к `Currency`.

Связь между пользователями и валютами реализована через `UserCurrency` как связь **«многие ко многим»**: один пользователь может быть подписан на несколько валют, и одна валюта может иметь несколько подписчиков.

---

## 3. Структура проекта

```text
myapp/
├── __init__.py
├── myapp.py                  # запуск сервера, маршрутизация (Controller)
├── models/                   # модели предметной области (Model)
│   ├── __init__.py
│   ├── author.py             # класс Author
│   ├── app.py                # класс App
│   ├── user.py               # класс User
│   ├── currency.py           # класс Currency
│   └── user_currency.py      # класс UserCurrency (связка User–Currency)
├── utils/
│   └── currencies_api.py     # функция get_currencies (работа с API ЦБ РФ)
└── templates/                # HTML-шаблоны (View)
    ├── index.html            # главная страница (/)
    ├── users.html            # список пользователей (/users)
    ├── user.html             # страница одного пользователя (/user?id=...)
    └── currencies.html       # список валют и курсов (/currencies)
```

## 4. Описание реализации
### 4.1. Модели и геттеры/сеттеры

Все модели находятся в пакете `models`. Для каждого поля реализованы:

  - приватный атрибут (например, `self.__name`);

  - геттер через `@property`;

  - сеттер через `@<name>.setter` с проверкой типов и корректности значений.

Пример (фрагмент класса `Currency`):
```python
class Currency:
    def __init__(self, id, num_code, char_code, name, value, nominal=1):
        self.id = id
        self.num_code = num_code
        self.char_code = char_code
        self.name = name
        self.value = value
        self.nominal = nominal

    @property
    def value(self) -> float:
        return self.__value

    @value.setter
    def value(self, value: float):
        if isinstance(value, (int, float)) and value >= 0:
            self.__value = float(value)
        else:
            raise ValueError("Курс валюты должен быть неотрицательным числом")
```

### 4.2. Маршрутизация и обработка запросов (Controller)

Для обработки HTTP-запросов используется стандартная библиотека:

- `HTTPServer` - запуск сервера;

- `BaseHTTPRequestHandler` - обработчик запросов;

- `urllib.parse` - разбор URL и query-параметров.

Основные маршруты:

- `/` - главная страница с информацией о приложении и авторе;

- `/users` - список пользователей;

- `/user?id=...` - страница конкретного пользователя и его подписок;

- `/currencies `- список валют и их текущих курсов;

- `/author` - страница с информацией об авторе.

Фрагмент обработчика:
```python
class MyRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)

        if path == "/":
            html = template_index.render(app=app_info, navigation=nav)
            self._send_html(html)

        elif path == "/users":
            html = template_users.render(app=app_info, users=USERS)
            self._send_html(html)

        elif path == "/user":
            # обработка /user?id=...
            ...

        elif path == "/currencies":
            update_currency_rates()
            html = template_currencies.render(app=app_info, currencies=CURRENCIES)
            self._send_html(html)

        else:
            self._send_html("<h1>404 Not Found</h1>", status=404)
```
### 4.3. Использование Jinja2 и Environment

Шаблонизатор Jinja2 инициализируется один раз при старте приложения:
```python
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader("myapp"),   # "myapp" - имя пакета с шаблонами
    autoescape=select_autoescape()
)

template_index = env.get_template("index.html")
template_users = env.get_template("users.html")
template_user = env.get_template("user.html")
template_currencies = env.get_template("currencies.html")
```

Это позволяет:

- кэшировать шаблоны и не загружать их каждый раз при запросе;

- рендерить один и тот же шаблон с разными данными.

Пример рендера главной страницы:
```python
html_content = template_index.render(
    app=app_info,
    navigation=[
        {"caption": "Главная", "href": "/"},
        {"caption": "Пользователи", "href": "/users"},
        {"caption": "Валюты", "href": "/currencies"},
    ],
)
```
### 4.4. Интеграция `get_currencies` и обновление курсов

Функция `get_currencies` реализована в `utils/currencies_api.py` и использует API ЦБ РФ (`https://www.cbr-xml-daily.ru/daily_json.js`).

Контроллер вызывает её при запросе `/currencies`:
```python
from utils.currencies_api import get_currencies
from models.currency import Currency

def update_currency_rates() -> None:
    codes = [c.char_code for c in CURRENCIES]
    data = get_currencies(codes)
    for c in CURRENCIES:
        if c.char_code in data:
            c.value = data[c.char_code]
```



То есть:

**1.** Собираются символьные коды валют (USD, EUR, GBP и т.д.);

**2.** Вызывается `get_currencies(codes)`;

**3.** Полученные значения записываются в объекты `Currency`.

## 5. Примеры работы приложения
### 5.1. Главная страница `/`
![index.jpg](img%2Findex.jpg)

### 5.2. Валюты 
![currencies.jpg](img%2Fcurrencies.jpg)

### 5.3. Подписки пользователя 
![user_id.jpg](img%2Fuser_id.jpg)

## 7. Тестирование
### 7.1. Тесты моделей

Проверяется:

- корректность геттеров/сеттеров;

- выброс `ValueError` при некорректных значениях.

Фрагмент:
```python
class TestUserModel(unittest.TestCase):
    def test_user_ok(self):
        u = User(1, "Алиса")
        self.assertEqual(u.id, 1)
        self.assertEqual(u.name, "Алиса")

    def test_user_invalid_id(self):
        with self.assertRaises(ValueError):
            User(0, "Алиса")
```

### 7.2. Тесты функции `get_currencies`

Для тестов используется `unittest.mock` - `requests.get` подменяется фейковым объектом, чтобы не ходить в реальный интернет.

Фрагмент:
```python
@patch("myapp.utils.currencies_api.requests.get")
def test_get_currencies_ok(self, mock_get):
    mock_resp = MagicMock()
    mock_resp.raise_for_status.return_value = None
    mock_resp.json.return_value = {
        "Valute": {"USD": {"Value": 90.5}}
    }
    mock_get.return_value = mock_resp

    result = get_currencies(["USD"])
    self.assertEqual(result["USD"], 90.5)
```


Проверяются также случаи:

- ошибка сети → `ConnectionError`;

- некорректный JSON → `ValueError`;

- отсутствие ключа `Valute` → `KeyError`;

- отсутствие нужной валюты → `KeyError`;

- неверный тип значения курса → `TypeError`.

### 7.3. Тесты контроллера (маршруты)

Поднимается тестовый HTTP-сервер в отдельном потоке и выполняются запросы:
```python
resp = requests.get(base_url + "/")
self.assertEqual(resp.status_code, 200)
self.assertIn("CurrenciesListApp", resp.text)

resp = requests.get(base_url + "/users")
self.assertEqual(resp.status_code, 200)

resp = requests.get(base_url + "/currencies")
self.assertEqual(resp.status_code, 200)

resp = requests.get(base_url + "/user?id=1")
self.assertEqual(resp.status_code, 200)
```

Проверяется также поведение при отсутствии `id` или неверном значении.

### 7.4. Тесты шаблонов

Через Jinja2 Environment рендерятся шаблоны и проверяется содержимое HTML:
```python
env = Environment(
    loader=PackageLoader("myapp"),
    autoescape=select_autoescape()
)

template = env.get_template("users.html")
html = template.render(app=app, users=[User(1, "Алиса")])

self.assertIn("Пользователи", html)
self.assertIn("Алиса", html)
self.assertIn("/user?id=1", html)
```
Скриншот

![test.jpg](img%2Ftest.jpg)

### 8. Выводы

В ходе работы я:

- реализовал **клиент-серверное приложение** на чистом `HTTPServer` без использования фреймворков;

- построил простую архитектуру **MVC**:
  - модели отвечают за данные и валидацию;

  - контроллер - за маршрутизацию и обработку запросов;

  - шаблоны Jinja2 - за отображение;

- интегрировал внешнее API курсов валют через функцию `get_currencies`, научился обрабатывать сетевые ошибки и ошибки формата данных;

- освоил инициализацию и использование Jinja2 через `Environment` и `PackageLoader`;

- написал набор тестов для моделей, функции `get_currencies`, контроллера и шаблонов, что помогло поймать ошибки на ранних этапах.

В итоге я лучше понял, как работают низкоуровневые HTTP-механизмы в Python, как использовать шаблонизатор Jinja2 и как интегрировать внешние API в собственное веб-приложение.
