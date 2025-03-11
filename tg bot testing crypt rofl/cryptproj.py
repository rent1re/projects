import requests
from bs4 import BeautifulSoup

# 1️⃣ Binance API
def get_binance_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    return float(data["price"])

# 2️⃣ BitInfoCharts (Парсинг HTML)
import re

def get_bitinfocharts_price():
    url = "https://bitinfocharts.com/ru/crypto-kurs/"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    table = soup.find("table", class_="table")
    if not table:
        raise ValueError("Таблица с курсами не найдена!")

    rows = table.find_all("tr")[1:]  # Пропускаем заголовок
    prices = {}

    for row in rows:
        cols = row.find_all("td")
        if len(cols) > 2:
            coin_name = cols[0].text.strip()  # Название монеты
            
            # Оставляем только число, убираем проценты и время (регулярка ищет число с точкой)
            price_match = re.search(r"\d+\.\d+", cols[1].text)
            if price_match:
                price = float(price_match.group())  # Берём только найденное число
                prices[coin_name] = price

    print("Спарсенные монеты:", prices.keys())  # Вывод списка монет
    return prices



# 3️⃣ Сравнение данных
def compare_prices(symbol="BTC"):
    binance_price = get_binance_price(symbol + "USDT")
    bitinfo_prices = get_bitinfocharts_price()

    print(f"Ищем {symbol} среди: {bitinfo_prices.keys()}")  # Отладка

    # Ищем ключ, который начинается с тикера (например, "BTC" → "BTC Bitcoin")
    bitinfo_key = next((key for key in bitinfo_prices if key.startswith(symbol + " ")), None)

    print(f"Найденный ключ: {bitinfo_key}")  # Отладка

    if bitinfo_key:
        bitinfo_price = bitinfo_prices[bitinfo_key]
        print(f"Цена с Binance: {binance_price}, Цена с BitInfoCharts: {bitinfo_price}")  # Отладка
        
        # Не умножаем цену с BitInfoCharts на курс Binance
        diff = abs(binance_price - bitinfo_price)
        percent_diff = (diff / binance_price) * 100

        return {
            "Binance": binance_price,
            "BitInfoCharts": bitinfo_price,
            "Разница": diff,
            "Процентное расхождение": f"{percent_diff:.2f}%"
        }
    else:
        return f"Монета {symbol} не найдена на BitInfoCharts!"

# 4️⃣ Тест
print(compare_prices("BTC"))
