import requests

# 1️⃣ Binance API
def get_binance_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    
    # Логируем ответ
    print(f"Ответ от Binance: {data}")
    
    # Проверяем, если в ответе есть ошибка
    if "code" in data:
        raise ValueError(f"Ошибка получения данных с Binance: {data}")
    
    return float(data["price"])

# 3️⃣ Сравнение данных
def compare_prices(symbol="BTC"):
    try:
        binance_price = get_binance_price(symbol + "USDT")
        print(f"Цена с Binance для {symbol}: {binance_price}")
    except ValueError as e:
        print(e)

# 4️⃣ Тест
compare_prices("BTC")  # Для Bitcoin
