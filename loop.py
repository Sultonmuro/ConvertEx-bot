import asyncio
import logging
import requests
from typing import Final
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
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

# Start command
@dp.message(Command("start"))

async def send_welcome(message: types.Message):
    await message.reply(
        "Welcome to **ConvertEx Bot! 🎉\n"
        "Добро пожаловать в **ConvertEx Bot! 🎉\n\n"
        "Use `/convert` to start converting currencies.\n"
        "Используйте `/convert`, чтобы начать конвертацию валют."
    )

# Convert command
@dp.message(Command("convert"))
async def convert(message: types.Message):
    await message.reply(
        "Please enter the amount you want to convert and the currency code you want to convert to.\n"
        "Пожалуйста, введите сумму, которую хотите конвертировать, и код валюты, в которую хотите конвертировать.\n\n"
        "**Format:** `<amount> <from_currency> <to_currency>`\n"
        "**Формат:** `<сумма> <из_валюты> <в_валюту>`\n\n"
        "**Example:** `10 USD INR`\n"
        "**Пример:** `10 USD INR`"
    )
# Handling conversion logic
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

# Main function
async def main():
    await dp.start_polling(bot)

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())










