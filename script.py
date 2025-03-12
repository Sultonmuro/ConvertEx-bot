import logging
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = "7716973064:AAFaK6MzvF5eJJfAjd-jv0zQu9Qv20Jsh4I"


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    await update.message.reply_text("Welcome to Epic Payments Bot! Use /payment to start a transaction.")


async def payment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send payment options inline keyboard."""
    keyboard = [
        [
            InlineKeyboardButton("Manual Amount", callback_data="manual"),
        ],
        [
            InlineKeyboardButton("$1", callback_data="1"),
            InlineKeyboardButton("$5", callback_data="5"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Please choose payment amount:", reply_markup=reply_markup)


async def handle_button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle inline keyboard button presses."""
    query = update.callback_query
    await query.answer()

    if query.data == "manual":
        context.user_data["expecting_amount"] = True
        await query.edit_message_text(text="Please enter your custom amount in dollars:")
    else:
        amount = query.data
        await handle_payment_amount(update, context, amount)

GROUP_CHAT_ID = "-1001234567890"  # Replace with your group chat ID
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle user messages."""
    user_data = context.user_data

    if user_data.get("expecting_amount"):
        try:
            amount = float(update.message.text)
            if amount <= 0:
                await update.message.reply_text("Please enter a positive amount.")
                return
            user_data["amount"] = amount
            user_data["expecting_amount"] = False
            await handle_payment_amount(update, context, amount)
        except ValueError:
            await update.message.reply_text("Please enter a valid number.")


    elif user_data.get("verification_pending"):
        if update.message.text == user_data.get("verification_code"):
            amount = user_data["amount"]
            await update.message.reply_text(f"✅ Payment of ${amount:.2f} successful! Thank you!")

            # New group invitation logic
            try:
                await context.bot.send_chat_action(
                    chat_id=GROUP_CHAT_ID,
                    action="add_chat_members"
                )
                await context.bot.add_chat_member(
                    chat_id=GROUP_CHAT_ID,
                    user_id=update.message.from_user.id
                )
                await update.message.reply_text(
                    "🎉 You've been added to the private group!\n"
                    "Please check your Telegram chats."
                )
            except Exception as e:
                logger.error(f"Error adding user to group: {e}")
                await update.message.reply_text(
                    "⚠️ Couldn't add you to the private group. "
                    "Please contact support."
                )

            user_data.clear()
        else:
            await update.message(f"❌ Incorrect verification code. Please try again.")
            user_data.clear()
    # ... [existing failed verification handling] ...


async def handle_payment_amount(update, context, amount):
    """Handle payment amount and generate verification."""
    if isinstance(amount, str):
        amount = float(amount)

    verification_code = str(random.randint(100000, 999999))
    context.user_data.update({
        "verification_pending": True,
        "verification_code": verification_code,
        "amount": amount
    })

    if isinstance(update, Update):  # For manual amount flow
        await update.message.reply_text(
            f"🔐 Verification code: {verification_code}\n"
            f"Please enter the code to confirm ${amount:.2f} payment."
        )
    else:  # For inline button flow
        await update.edit_message_text(
            f"🔐 Verification code: {verification_code}\n"
            f"Please enter the code to confirm ${amount:.2f} payment."
        )


def main() -> None:
    """Start the bot."""
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("payment", payment))
    application.add_handler(CallbackQueryHandler(handle_button))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    application.run_polling()


if __name__ == "__main__":
    main()