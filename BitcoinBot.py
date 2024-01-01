from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from prettytable import PrettyTable
import requests

TOKEN = "6727030368:AAHVoZc9XxoFioqHCQZ-VJU4_nwyBBJXUNs"

def start(update, context):
    user = update.effective_user
    update.message.reply_html(
        fr"Привет {user.mention_html()}!",
        reply_markup=main_menu(),
    )

def main_menu():
    keyboard = [
        [InlineKeyboardButton("Курсы криптовалют", callback_data='get_crypto')],
    ]
    return InlineKeyboardMarkup(keyboard)

def button(update, context):
    query = update.callback_query
    query.answer()

    if query.data == 'get_crypto':
        get_crypto(update, context)

def get_crypto(update, context):
    try:
        response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,ripple,litecoin,cardano,polkadot,stellar,chainlink,binancecoin,usd-coin&vs_currencies=usd')
        data = response.json()

        table = PrettyTable()
        table.field_names = ["Криптовалюта", "Курс в USD"]

        for crypto, rate in data.items():
            table.add_row([crypto.capitalize(), f"${rate['usd']}"])

        if update.message:
            update.message.reply_text(f"<pre>{table}</pre>", parse_mode='HTML')
        elif update.callback_query and update.callback_query.message:
            update.callback_query.message.reply_text(f"<pre>{table}</pre>", parse_mode='HTML')

    except Exception as e:
        error_message = f'Ошибка при получении курсов криптовалют: {e}'
        if update.message:
            update.message.reply_text(error_message)
        elif update.callback_query and update.callback_query.message:
            update.callback_query.message.reply_text(error_message)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
