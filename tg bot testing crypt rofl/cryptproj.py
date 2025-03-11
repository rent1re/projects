import requests
from bs4 import BeautifulSoup

# 1️⃣ Получаем цену с CoinGecko
def get_coingecko_price(symbol="bitcoin"):
    url = f"https://www.coingecko.com/ru/криптовалюты/{symbol}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Ищем цену на странице
    price_tag = soup.find("span", class_="no-wrap")
    if price_tag:
        price = price_tag.text.strip().replace("₽", "").replace(",", "")
        return float(price)
    else:
        raise ValueError("Не удалось найти цену на CoinGecko!")

# 2️⃣ Binance API (с отладкой)
# 1️⃣ Binance API (с отладкой)
def get_binance_price(symbol="BTCUSDT"):
    symbol = symbol.upper()  # Преобразуем символ в верхний регистр
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    response = requests.get(url)
    data = response.json()

    # Выводим отладочную информацию
    print("Ответ от Binance:", data)

    if "price" in data:
        return float(data["price"])
    else:
        raise ValueError(f"Ошибка получения данных с Binance: {data}")

# 3️⃣ Сравнение цен
def compare_prices(symbol="BTC"):
    binance_price = get_binance_price(symbol + "USDT")
    try:
        coingecko_price = get_coingecko_price(symbol.lower())
    except Exception as e:
        return str(e)

    print(f"Ищем {symbol} среди: CoinGecko и Binance")
    
    print(f"Цена с Binance: {binance_price}, Цена с CoinGecko: {coingecko_price}")
    
    diff = abs(binance_price - coingecko_price)
    percent_diff = (diff / binance_price) * 100

    return {
        "Binance": binance_price,
        "CoinGecko": coingecko_price,
        "Разница": diff,
        "Процентное расхождение": f"{percent_diff:.2f}%"
    }

# 4️⃣ Тестируем
print(compare_prices("BTC"))  # Для Bitcoin
