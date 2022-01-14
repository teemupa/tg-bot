#!/usr/bin/env python3

from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram import ParseMode
from ruuvi import Ruuvi
import config
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    if is_me(user):
        context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def ruuvi(update: Update, context: CallbackContext):
    user = update.message.from_user
    logging.info('Ruuvi query from user %s', user)
    if is_me(user):
        ruuvi = Ruuvi()
        data = ruuvi.get_all()
        if data:
            for key in data:
                if key == 'sauna':
                    title = "<b>Sauna</b>"
                elif key == 'indoor':
                    title = "<b>Indoors</b>"
                elif key == 'outdoor':
                    title = "<b>Outdoors</b>"
                body = ("\n\U0001f321 " + str(data[key]['temperature']) + "\u00b0C" +
                        "\n\U0001F4A7 " + str(data[key]['humidity']) + "%" + 
                        "\n\U0001F4A8 " + str(data[key]['pressure']) + "hPa" + 
                        "\n\U0001F550 " + str(data[key]['time'])
                        )
                context.bot.send_message(chat_id=update.effective_chat.id, text=title + body, parse_mode=ParseMode.HTML)
        else:
            logging.error('Query of Ruuvi database failed.')
            
def is_me(user):
    #TODO Can I use a filter to filter requests only from me?
    if user['id'] == config.me:
        return True
    return False

def main():
    updater = Updater(token=config.token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('ruuvi', ruuvi))

    updater.start_polling()

if __name__ == "__main__":
    main()