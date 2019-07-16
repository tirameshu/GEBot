from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from scraper import scraping
import logging
import os
import json
import requests

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

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def respond(bot, update):
    postal_code = update.message.text
    if ("win" in postal_code) or ("election" in postal_code):
        msg = "Sorry there's no public information on this. Democracy is uncertain. :/"
    elif (isValid(postal_code)):
        # make https req
        url = "https://sggrc.herokuapp.com/postcode/" + postal_code
        js = get_json_from_url(url)
        grc = js["grc"]
        members = scraping(grc)
        if (len(members) > 1):
            names = ', '.join(members)
            msg = "Your GRC is " + grc + " and your MPs are: " + names
        elif (len(members) == 1):
            msg = "Your SMC is " + grc + " and your MP is: " + members[0]
        else:
            msg = "Postal code does not exist/ not yet in database!"
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
