import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Настроим логирование
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен твоего бота
TOKEN = "8060036697:AAGakBUZ_Xa8HTZzhy0uub4GNk2mmw8wM7Q"  # Вставь свой токен

# Функция для получения данных о криптовалюте с Binance
def get_binance_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    try:
        response = requests.get(url)
        data = response.json()
        return float(data["price"]) if "price" in data else None
    except Exception as e:
        logger.error(f"Ошибка Binance: {e}")
        return None

# Функция для получения данных с CoinGecko
def get_coingecko_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    try:
        response = requests.get(url)
        data = response.json()
        return data.get(symbol, {}).get("usd")
    except Exception as e:
        logger.error(f"Ошибка CoinGecko: {e}")
        return None

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я показываю цены криптовалют.\nНапиши /prices, чтобы получить актуальные цены.")

# Команда /prices
async def get_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    coins = {"bitcoin": "BTC", "ethereum": "ETH", "binancecoin": "BNB", "cardano": "ADA", "ripple": "XRP"}

    message = "Цены криптовалют:\n\n"
    for coingecko_symbol, binance_symbol in coins.items():
        binance_price = get_binance_price(binance_symbol)
        coingecko_price = get_coingecko_price(coingecko_symbol)

        if binance_price and coingecko_price:
            diff = abs(binance_price - coingecko_price)
            percent_diff = (diff / binance_price) * 100
            message += (
                f"🔹 {binance_symbol}:\n"
                f"📌 Binance: {binance_price}$\n"
                f"📌 CoinGecko: {coingecko_price}$\n"
                f"⚖ Разница: {diff:.2f}$ ({percent_diff:.2f}%)\n\n"
            )

    await update.message.reply_text(message if message.strip() else "Ошибка получения данных 😢")

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prices", get_prices))

    app.run_polling()

if __name__ == "__main__":
    main()
