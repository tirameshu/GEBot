from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import os

NAME = "gebot"
TOKEN=os.environ['TOKEN']
PORT = os.environ.get('PORT', '5000')

updater = Updater(TOKEN)
dp = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, send me a postal code and I'll tell you about your electoral district!")

start_handler = CommandHandler('start', start)
dp.add_handler(start_handler)

def isValid(postal_code):
    if (len(postal_code) == 6):
        try:
            int(postal_code)
            return True
        except ValueError:
            return False
    return False

def respond(bot, update):
    postal_code = update.message.text
    if (isValid(postal_code)):
        # make https req
        msg = "Your GRC is... Your MP is..."
    else:
        msg = "Invalid postal code!"
    bot.send_message(chat_id=update.message.chat_id, text=msg)

respond_handler = MessageHandler(Filters.text, respond)
dp.add_handler(respond_handler)

def echo(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=update.message.text)

echo_handler = MessageHandler(Filters.text, echo)
dp.add_handler(echo_handler)

# start webhooks
updater.start_webhook(listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN)
updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
updater.idle()

# start locally
# updater.start_polling()
