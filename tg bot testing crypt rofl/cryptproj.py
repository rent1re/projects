import requests
from bs4 import BeautifulSoup
import re

# 1️⃣ Binance API
def get_binance_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()

    if 'price' in data:
        return float(data["price"])
    else:
        raise ValueError(f"Ошибка получения данных с Binance: {data}")

# 2️⃣ Парсинг с CoinGecko
def get_coingecko_price(symbol="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()

    if symbol in data:
        return data[symbol]["usd"]
    else:
        raise ValueError(f"Ошибка получения данных с CoinGecko для {symbol}: {data}")

# 3️⃣ Парсинг с BitInfoCharts (HTML)
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
            price_match = re.search(r"\d+\.\d+", cols[1].text)
            if price_match:
                price = float(price_match.group())  # Берём только найденное число
                prices[coin_name] = price

    return prices

# 4️⃣ Сравнение цен
def compare_prices(symbol="bitcoin"):
    try:
        binance_symbol = "BTCUSDT" if symbol.lower() == "bitcoin" else symbol.upper() + "USDT"
        binance_price = get_binance_price(binance_symbol)
    except ValueError as e:
        print(f"Ошибка получения данных с Binance: {e}")
        binance_price = None

    try:
        coingecko_price = get_coingecko_price(symbol.lower())  # Преобразуем в нижний регистр для CoinGecko
    except ValueError as e:
        print(f"Ошибка получения данных с CoinGecko: {e}")
        coingecko_price = None

    try:
        bitinfo_prices = get_bitinfocharts_price()
    except ValueError as e:
        print(f"Ошибка получения данных с BitInfoCharts: {e}")
        bitinfo_prices = {}

    if binance_price and coingecko_price and bitinfo_prices:
        print(f"Цена с Binance для {symbol}: {binance_price}")
        print(f"Цена с CoinGecko для {symbol}: {coingecko_price}")

        # Улучшенный поиск для BitInfoCharts
        bitinfo_key = next((key for key in bitinfo_prices if "BTC" in key or "Bitcoin" in key), None)
        if bitinfo_key:
            bitinfo_price = bitinfo_prices[bitinfo_key]
            print(f"Цена с BitInfoCharts для {symbol}: {bitinfo_price}")

            diff = abs(binance_price - bitinfo_price)
            percent_diff = (diff / binance_price) * 100

            return {
                "Binance": binance_price,
                "CoinGecko": coingecko_price,
                "BitInfoCharts": bitinfo_price,
                "Разница": diff,
                "Процентное расхождение": f"{percent_diff:.2f}%"
            }
        else:
            return f"Монета {symbol} не найдена на BitInfoCharts!"
    else:
        return "Ошибка получения данных с одного из источников."

# 5️⃣ Тестируем с BTC
print(compare_prices("bitcoin"))
