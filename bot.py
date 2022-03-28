#!/usr/bin/env python3

from telegram.ext import Updater
from telegram import Update
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram import ParseMode
from ruuvi import Ruuvi
from ski_tracks import SkiTracks
from f1 import F1
import config
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def ruuvi(update: Update, context: CallbackContext):
    user = update.message.from_user
    logging.info("/ruuvi command from user %s", user)
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
        context.bot.send_message(chat_id=update.effective_chat.id, text="ERROR: Ruuvi query failed!", parse_mode=ParseMode.HTML)
        logging.error("/ruuvi command query failed.")

def latu(update: Update, context: CallbackContext):
    user = update.message.from_user
    logging.info("/latu command received from user %s", user)
    tracks = SkiTracks()
    data = tracks.maintenance_status()
    message = ""
    if data:
        for i in data:
            message = message + "\n \U0001F3BF <b>" + i[0] + ":</b> \n" + str(i[1]) + "\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="ERROR: Maintenance status not found!", parse_mode=ParseMode.HTML)

def f1(update: Update, context: CallbackContext):
    f1 = F1()
    logging.info("/f1 command with args: %s", str(context.args))
    standings = []
    season = []
    message = ""

    if len(context.args) == 1:
        arg = context.args[0]
        if arg == 'drivers':
            standings = f1.driver_standings()
            message = "<b>#\tName\tPoints</b>"
        elif arg == 'teams':
            standings = f1.constructor_standings()
            message = "<b>#\tTeam\tPoints</b>"
        elif arg == 'season':
            season = f1.season()
            message = '<b>Season calendar</b>'
        else:
            message = "ERROR: No such argument!"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)
            return

        if (arg == 'drivers' or arg == 'teams') and standings:
            for i in standings:
                message = message + '\n' + i[0] + '. ' + i[2] + ' ' + i[1]
        elif arg == 'season' and season:
            for i in season:
                message = message + '\n' + i[0] + ': ' + i[1]
        else:
            message = "ERROR: Unable to fetch f1 data!"
    else:
        message = "usage: /f1 teams|drivers|season"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)



def main():
    updater = Updater(token=config.token, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('ruuvi', ruuvi, Filters.user(username=config.users)))
    dispatcher.add_handler(CommandHandler('latu', latu, Filters.user(username=config.users)))
    dispatcher.add_handler(CommandHandler('f1', f1, Filters.user(username=config.users)))

    updater.start_polling()

if __name__ == "__main__":
    main()