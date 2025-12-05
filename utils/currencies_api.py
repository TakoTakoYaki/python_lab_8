import requests


CBR_DAILY_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def get_currencies(currency_codes: list[str],
                   url: str = CBR_DAILY_URL,
                   timeout: float = 5.0) -> dict[str, float]:
    """
    Получает курсы валют по списку кодов, например ['USD', 'EUR'].

    Возвращает словарь {"USD": 93.25, "EUR": 101.7}

    Исключения:
      - ConnectionError  — проблемы с запросом
      - ValueError       — некорректный JSON
      - KeyError         — нет ключа Valute или конкретной валюты
      - TypeError        — неверный тип курса в JSON
    """
    try:
        resp = requests.get(url, timeout=timeout)
        resp.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"API request error: {e}") from e

    try:
        data = resp.json()
    except ValueError as e:
        raise ValueError("Invalid JSON from API") from e

    if "Valute" not in data:
        raise KeyError("Valute")

    valute = data["Valute"]
    result: dict[str, float] = {}

    for code in currency_codes:
        if code not in valute:
            raise KeyError(f"Currency code '{code}' is missing in API data")
        raw_val = valute[code].get("Value")
        if not isinstance(raw_val, (int, float)):
            raise TypeError(
                f"Currency rate for '{code}' must be numeric, got {type(raw_val).__name__}"
            )
        result[code] = float(raw_val)

    return result
