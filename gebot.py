<<<<<<< HEAD
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from private import TOKEN
import logging
import os

NAME = "shielded-anchorage-59750"
PORT = os.environ.get('PORT', '5000')

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

# start webhooks
updater.start_webhook(listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN)
updater.bot.setWebhook("https://{}.herokuapp.com/{}".format(NAME, TOKEN))
updater.idle()

# start locally
# updater.start_polling()
=======
import json
import requests
import time
import urllib
from dbhelper import DBHelper

db = DBHelper()

TOKEN = "814646941:AAFI3MkVyYz4gOq1oTkUvPmy5zNMX7HS_Sg"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    return (text, chat_id)

def handle_updates(updates):
    for update in updates["result"]:
        postal_code = update["message"]["text"]
        chat = update["message"]["chat"]["id"]
        info = db.get_items(postal_code)
        if info: # get_items returns a 1-d list
            message = info[0]
        else:
            message = "Sorry the postal code is not in database. I will inform my developer!"
            # send_message(help_message, me)
        print("information obtained: ")
        print(info)
        send_message(message, chat)

def send_message(text, chat_id):
    text = urllib.parse.quote_plus(text)
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    get_url(url)

def main():
    db.setup()
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if len(updates["result"]) > 0:
            last_update_id = get_last_update_id(updates) + 1
            handle_updates(updates)

if __name__ == '__main__':
    main()
>>>>>>> c7e0cd96e1c1e8eddaf8117f7da23b422c133046
