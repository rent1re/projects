import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import requests
import asyncio

# Настроим логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен твоего бота
TOKEN = "8060036697:AAGakBUZ_Xa8HTZzhy0uub4GNk2mmw8wM7Q"  # Обязательно вставь свой токен

# Функция для получения данных о криптовалюте с Binance
def get_binance_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    try:
        response = requests.get(url)
        data = response.json()
        if "price" in data:
            return float(data["price"])
        else:
            logger.error(f"Ошибка получения данных с Binance: {data}")
            return None
    except Exception as e:
        logger.error(f"Ошибка получения данных с Binance: {e}")
        return None

# Функция для получения данных с CoinGecko
def get_coingecko_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        if symbol in data:
            return data[symbol]["usd"]
        else:
            logger.error(f"Ошибка получения данных с CoinGecko для {symbol}: {data}")
            return None
    except Exception as e:
        logger.error(f"Ошибка получения данных с CoinGecko: {e}")
        return None

# Функция для обработки команд
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Привет! Я могу показать цены криптовалют.")

# Функция для получения и отображения цен криптовалют
async def get_prices(update: Update, context: CallbackContext):
    coins = ['bitcoin', 'ethereum', 'binancecoin', 'cardano', 'ripple']
    
    prices = {}

    for coin in coins:
        binance_price = get_binance_price(coin.upper())  # Binance требует символ в верхнем регистре
        coingecko_price = get_coingecko_price(coin)

        if binance_price is not None and coingecko_price is not None:
            difference = abs(binance_price - coingecko_price)
            percentage_diff = (difference / binance_price) * 100
            prices[coin] = {
                "Binance": binance_price,
                "CoinGecko": coingecko_price,
                "Разница": difference,
                "Процентное расхождение": f"{percentage_diff:.2f}%",
            }

    # Формируем сообщение для пользователя
    message = "Цены криптовалют:\n\n"
    for coin, data in prices.items():
        message += f"{coin.capitalize()}:\n"
        message += f"Binance: {data['Binance']}\n"
        message += f"CoinGecko: {data['CoinGecko']}\n"
        message += f"Разница: {data['Разница']}\n"
        message += f"Процентное расхождение: {data['Процентное расхождение']}\n\n"

    # Отправляем сообщение
    await update.message.reply_text(message)

# Основная функция для запуска бота
def main():
    # Инициализация приложения
    application = Application.builder().token(TOKEN).build()

    # Команды
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("prices", get_prices))

    # Запуск бота с polling
    application.run_polling(timeout=10, read_timeout=10)

if __name__ == '__main__':
    main()
