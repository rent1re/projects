import requests

# Функция для получения цены с Binance (используя API)
def get_binance_price(symbol="BTCUSDT"):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    response = requests.get(url)
    data = response.json()
    if 'price' in data:
        return float(data["price"])
    else:
        raise ValueError(f"Ошибка получения данных с Binance: {data}")

# Функция для получения цены с CoinGecko (используя API)
def get_coingecko_price(symbol="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    if symbol in data:
        return data[symbol]['usd']
    else:
        raise ValueError(f"Ошибка получения данных с CoinGecko для {symbol}: {data}")

# Функция для вычисления процентного расхождения
def calculate_percentage_difference(price1, price2):
    return abs(price1 - price2) / price1 * 100

# Список популярных криптовалют и их тикеров для Binance
coins = {
    "bitcoin": "BTCUSDT",
    "ethereum": "ETHUSDT",
    "binancecoin": "BNBUSDT",
    "cardano": "ADAUSDT",
    "ripple": "XRPUSDT"
}

# Обрабатываем каждую криптовалюту
for coin, binance_ticker in coins.items():
    try:
        # Получаем цену с Binance
        binance_price = get_binance_price(binance_ticker)
        print(f"Цена с Binance для {coin}: {binance_price}")

        # Получаем цену с CoinGecko
        coingecko_price = get_coingecko_price(coin)
        print(f"Цена с CoinGecko для {coin}: {coingecko_price}")

        # Вычисляем процентное расхождение
        percent_diff = calculate_percentage_difference(binance_price, coingecko_price)
        print(f"Процентное расхождение между Binance и CoinGecko для {coin}: {percent_diff:.2f}%")
        print("-" * 50)

    except Exception as e:
        print(f"Ошибка получения данных для {coin}: {e}")
        print("-" * 50)
