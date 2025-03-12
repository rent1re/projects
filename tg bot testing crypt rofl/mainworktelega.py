import logging
import aiohttp  # Для асинхронных HTTP-запросов
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

# Настроим логирование
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен твоего бота
TOKEN = "8060036697:AAGakBUZ_Xa8HTZzhy0uub4GNk2mmw8wM7Q"  # Вставь свой токен

# Список монет
coins = {
    "bitcoin": "BTC",
    "ethereum": "ETH",
    "binancecoin": "BNB",
    "cardano": "ADA",
    "ripple": "XRP"
}

# Функция для асинхронного запроса к Binance
async def get_binance_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                data = await response.json()
                return float(data["price"]) if "price" in data else None
        except Exception as e:
            logger.error(f"Ошибка Binance: {e}")
            return None

# Функция для асинхронного запроса к CoinGecko
async def get_coingecko_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                data = await response.json()
                return data.get(symbol, {}).get("usd")
        except Exception as e:
            logger.error(f"Ошибка CoinGecko: {e}")
            return None

# Команда /start с кнопками
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 Узнать цены", callback_data="get_prices")],
        [
            InlineKeyboardButton("🌐 Binance", url="https://www.binance.com/"),
            InlineKeyboardButton("🌍 CoinGecko", url="https://www.coingecko.com/")
        ],
        [InlineKeyboardButton("❓ Помощь", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Я показываю цены криптовалют. Выбери действие:", reply_markup=reply_markup)

# Функция для получения и отображения цен криптовалют
async def get_prices(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Подтверждаем нажатие кнопки

    # Запрашиваем все цены одновременно
    binance_tasks = {symbol: get_binance_price(ticker) for symbol, ticker in coins.items()}
    coingecko_tasks = {symbol: get_coingecko_price(symbol) for symbol in coins.keys()}

    binance_prices = await asyncio.gather(*binance_tasks.values())
    coingecko_prices = await asyncio.gather(*coingecko_tasks.values())

    # Формируем сообщение с HTML-разметкой
    message = "📈 <b>Текущие цены криптовалют:</b>\n\n"
    buttons = []

    for (coingecko_symbol, binance_symbol), binance_price, coingecko_price in zip(coins.items(), binance_prices, coingecko_prices):
        if binance_price and coingecko_price:
            diff = abs(binance_price - coingecko_price)
            percent_diff = (diff / binance_price) * 100
            message += (
                f"🔹 <b>{binance_symbol}</b>\n"
                f"📌 Binance: <code>{binance_price:.2f}$</code>\n"
                f"📌 CoinGecko: <code>{coingecko_price:.2f}$</code>\n"
                f"⚖ Разница: <code>{diff:.2f}$ ({percent_diff:.2f}%)</code>\n\n"
            )

            # Кнопки для каждой монеты
            buttons.append([
                InlineKeyboardButton(f"📈 {binance_symbol} на Binance", url=f"https://www.binance.com/en/trade/{binance_symbol}_USDT"),
                InlineKeyboardButton(f"📊 {binance_symbol} на CoinGecko", url=f"https://www.coingecko.com/en/coins/{coingecko_symbol}")
            ])

    buttons.append([InlineKeyboardButton("🔙 Назад в меню", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(buttons)

    await query.message.edit_text(message, reply_markup=reply_markup, parse_mode="HTML")

    # Создаём клавиатуру
    buttons.append([InlineKeyboardButton("🔙 Назад в меню", callback_data="start")])
    reply_markup = InlineKeyboardMarkup(buttons)

    await query.message.edit_text(message if message.strip() else "Ошибка получения данных 😢", reply_markup=reply_markup)

# Функция для обработки команды помощи
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.edit_text(
            "ℹ <b>Доступные команды:</b>\n"
            "/start - Главное меню 📌\n"
            "/prices - Узнать цены криптовалют 📈\n",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Назад", callback_data="start")]])
        )
    else:
        await update.message.reply_text(
            "ℹ <b>Доступные команды:</b>\n"
            "/start - Главное меню 📌\n"
            "/prices - Узнать цены криптовалют 📈\n",
            parse_mode="HTML"
        )

# Запуск бота
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    # Обработчики команд
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("prices", get_prices))
    app.add_handler(CommandHandler("help", help_command))

    # Обработчик нажатий кнопок
    app.add_handler(CallbackQueryHandler(get_prices, pattern="get_prices"))
    app.add_handler(CallbackQueryHandler(help_command, pattern="help"))
    app.add_handler(CallbackQueryHandler(start, pattern="start"))

    app.run_polling()

if __name__ == "__main__":
    import asyncio
    main()
