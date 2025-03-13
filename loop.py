import asyncio
import logging
import requests
from typing import Final
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,CallbackQuery

# Constants
TOKEN: Final = "7976994360:AAHhaW7XbqFC1nDABn5X7wllpMOGZWvVw7U"
BOT_USERNAME: Final = "@currencyConverter_bot_bot"
API_KEY: Final = "558d3841e6e1aae56c54db7b"
API_URL: Final = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/"

# Logging setup
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))

async def send_welcome(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton (text="convert", callback_data = "convert")
            ]
        ]
    )
    await message.reply(
        "Welcome to **ConvertEx Bot! 🎉\n"
        "Добро пожаловать в **ConvertEx Bot! 🎉\n\n"
        "Press convert button to start currency conversion.\n"
        "Нажмите на кнопку convert, чтобы начать конвертацию валют.",
        reply_markup=keyboard
    )


@dp.message(Command("convert"))
async def convert(message: types.Message):

    await message.reply(
        "Please enter the amount you want to convert and the currency code you want to convert to.\n"
        "Пожалуйста, введите сумму, которую хотите конвертировать, и код валюты, в которую хотите конвертировать.\n\n"
        "**Format:** `<amount> <from_currency> <to_currency>`\n"
        "**Формат:** `<сумма> <из_валюты> <в_валюту>`\n\n"
        "**Example:** `10 USD INR`\n"
        "**Пример:** `10 USD INR`",
    )

@dp.message(Command("help"))
async def send_help(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="start", callback_data="start"),
                InlineKeyboardButton(text="About", callback_data="about"),
                InlineKeyboardButton(text="Help", callback_data="help"),
                InlineKeyboardButton(text="convert", callback_data="convert"),
            ]
        ]
    )
    await message.reply(
        "**ConvertEx Bot Commands:**\n"
        "**Команды ConvertEx Bot:**\n\n"
        "`/start` - Start the bot(Запустить бота)\n"
        "`/convert` - Convert currencies(Конвертировать валюты)\n"
        "`/help` - Show help message(Помочь)\n"
        "`/about` - Show information about the bot(Показать информацию о боте)\n",
        reply_markup = keyboard
    )


@dp.message(Command("about"))
async def send_about(message: types.Message):
    await message.reply(
       "This bot uses the ExchangeRate-API to provide currency conversion rates.\n"
    )
@dp.callback_query()
async def handle_callBack(query: CallbackQuery):
    data = query.data
    if data =="start":
       await send_welcome(query.message)
    elif data == "about":
        await send_about(query.message)
    elif data == "help":
        await send_help(query.message)
    elif data == "convert":
        await convert(query.message)
@dp.message()
async def handle_conversion(message: types.Message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise ValueError("Invalid format")

        amount, from_currency, to_currency = parts
        amount = float(amount)


        response = requests.get(f"{API_URL}{from_currency.upper()}")
        if response.status_code != 200:
            await message.reply("Error fetching data from the API. Please try again later.")
            return

        data = response.json()
        if to_currency.upper() not in data['conversion_rates']:
            await message.reply("Invalid currency code. Please check and try again.")
            return


        rate = data['conversion_rates'][to_currency.upper()]
        converted_amount = amount * rate
        await message.reply(f"{amount} {from_currency.upper()} is **{converted_amount:.2f} {to_currency.upper()}**.")

    except ValueError:
        await message.reply("Invalid input format. Use: `<amount> <from_currency> <to_currency>` (e.g., `100 USD EUR`).")
    except Exception as e:
        logging.error(f"Error: {e}")
        await message.reply("An unexpected error occurred. Please try again.")


async def main():
    await dp.start_polling(bot)

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())










