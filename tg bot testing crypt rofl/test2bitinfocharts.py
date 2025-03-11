import requests
from bs4 import BeautifulSoup
import re

def get_bitinfocharts_price():
    url = "https://bitinfocharts.com/ru/crypto-kurs/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Найдем таблицу с курсами
    table = soup.find("table", class_="table")
    if not table:
        raise ValueError("Таблица с курсами не найдена!")

    rows = table.find_all("tr")[1:]  # Пропускаем заголовок
    prices = {}

    # Ищем нужные данные (не ссылки, а прямые цены)
    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 2:
            coin_name = cols[0].text.strip()  # Название монеты
            price_text = cols[1].text.strip()

            # Печатаем отладочную информацию
            print(f"Монета: {coin_name}, Цена: {price_text}")

            # Очищаем строку от ненужных символов и процентов
            price_cleaned = re.sub(r"[^\d.,]", "", price_text)  # Убираем все, кроме цифр и запятой
            if price_cleaned:
                try:
                    # Преобразуем цену в число
                    price = float(price_cleaned.replace(",", "."))
                    prices[coin_name] = price
                except ValueError:
                    print(f"Не удалось преобразовать цену: {price_cleaned}")
                    continue  # Если не удалось преобразовать в число, пропускаем

    print("Парсинг завершён!")
    if not prices:
        print("Не удалось получить цены!")
    else:
        print("Монеты и их цены:")
        for coin, price in prices.items():
            print(f"{coin}: {price}")

    return prices

# Пример вызова
prices = get_bitinfocharts_price()
