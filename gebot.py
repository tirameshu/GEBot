from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from private import TOKEN
import logging

NAME = shielded-anchorage-59750

updater = Updater(token=TOKEN)
dp = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, please send me a postal code!")

start_handler = CommandHandler('start', start)
dp.add_handler(start_handler)

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)
echo_handler = MessageHandler(Filters.text, echo)
dp.add_handler(echo_handler)

updater.start_polling()
