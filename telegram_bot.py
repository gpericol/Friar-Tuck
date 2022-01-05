#!/usr/bin/env python
# pylint: disable=C0116,W0613
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import Update, ForceReply, ParseMode
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

import psutil
import subprocess

import os
from telegram.utils.helpers import effective_message_type
from data.config.config import *
from os import remove, system
from os.path import exists
import json

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

def check_process_up():
    if not exists(CONFIG["path_pid"]):
        return False
    
    with open(CONFIG["path_pid"], 'r') as pid_file:
        pid = int(pid_file.read())

    # program crashed
    if not psutil.pid_exists(pid):
        remove(CONFIG["path_pid"])
        return False

    return True


def acl(func):
    def inner(update: Update, context: CallbackContext):
        print(update.effective_user)
        if update.effective_user.id in CONFIG["telegram_users"]:
            return func(update, context)
        else:
             update.message.reply_text("I don't know you, I'm not that kind of bot!")
    return inner


@acl
def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_markdown_v2(
        fr'Hi {user.mention_markdown_v2()}\!',
        reply_markup=ForceReply(selective=True),
    )

@acl
def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""

    update.message.reply_text('''
*Commands*
/status - check status
/terminate - stop thermostat
/list - available curves
/smart <curve id> <threshold>
/dsmart <curve id> <threshold> <delay>
/static <temperature> <threshold>
        '''
    , parse_mode=ParseMode.MARKDOWN)

@acl
def status_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(compose_status(), parse_mode=ParseMode.MARKDOWN)

@acl
def list_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(list_curves(), parse_mode=ParseMode.MARKDOWN)

@acl
def terminate_command(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(terminate())

@acl
def smart_command(update: Update, context: CallbackContext) -> None:
    result = ""
    values = update.effective_message.text.split()
    
    if len(values) != 3 or not values[1].isdigit() or not values[2].isdigit():
        update.message.reply_text("/smart <id> <threshold>")
    else:
        update.message.reply_text(launch_smart(int(values[1]),int(values[2])))

@acl
def dsmart_command(update: Update, context: CallbackContext) -> None:
    result = ""
    values = update.effective_message.text.split()
    
    if len(values) != 4 or not values[1].isdigit() or not values[2].isdigit() or not values[3].isdigit():
        update.message.reply_text("/dsmart <id> <threshold> <delay>")
    else:
        update.message.reply_text(launch_smart(int(values[1]),int(values[2])))

@acl
def static_command(update: Update, context: CallbackContext) -> None:
    result = ""
    values = update.effective_message.text.split()
    if len(values) != 3 or not values[1].isdigit() or not values[2].isdigit():
        update.message.reply_text("/static <id> <threshold>")
    else:
        update.message.reply_text(launch_static(int(values[1]),int(values[2])))
    

def compose_status():
    if not check_process_up():
        return "Friar Tuck is sleeping. /help"

    result = "Friar Tuck is running\n"
    with open(CONFIG["path_status"], 'r') as status_file:
        data = json.load(status_file)

        if data["type"] == "smart":
            result += "*mode* Smart\n"
            result += f'*threshold* ±{data["threshold"]}°C\n'
            result += f'*curve name* { data["curve_name"] }\n'
            if data["smart_mode"]:
                result += "*smart mode type* curve\n"
            else:
                result += "*smart mode type* ramp up\n"
            
            result += f'*running time* { data["running_time"]}h\n'
            
        else:
            result += "*mode* Static\n"
            result += f'*threshold* ±{data["threshold"]}°C\n'
            result += f'*target temperature* ±{data["target_temperature"]}°C\n'

        result += f"*temperature* {data['hardware_status']['temperature']}°C\n"
        result += f"*heater* {data['hardware_status']['heater']}\n"
        result += f"*cooler* {data['hardware_status']['cooler']}"
    result += "\n/help" 
    return result

def list_curves():
    result = ""
    with open(CONFIG["path_curves_list"], 'r') as curves_list_file:
        data = json.load(curves_list_file)

        for curve in data["curves"]:
            result += f'*{curve["id"]} - {curve["name"]}*\n{curve["description"]}\n---\n'
    
    result += "/help" 
    return result

def terminate():
    if not check_process_up():
        return "Friar Tuck already is sleeping. /help"
        
    remove(CONFIG["path_pid"])
    return "Friar Tuck was put to sleep. /help"

def launch_smart(curve_id, threshold, delay=0):
    if check_process_up():
        return "Friar Tuck is already working. /help"
        
    with open(CONFIG["path_curves_list"], 'r') as curves_list_file:
        data = json.load(curves_list_file)
        if curve_id not in range(0, len(data["curves"])):
            return "Friar Tuck doesn't know the curve you are looking for"
            
    if delay > 0:
        exec_params = ['python', 'friar_tuck.py','--delayed_curve', str(curve_id), str(threshold), str(delay)]
    else:
        exec_params = ['python', 'friar_tuck.py','--curve', str(curve_id), str(threshold)]
    
    subprocess.Popen(exec_params, stdout=subprocess.PIPE, shell=False)
    return "Friar Tuck is at work. /help"

def launch_static(temperature, threshold):
    if check_process_up():
         return "Friar Tuck is already working. /help"

    subprocess.Popen(['python', 'friar_tuck.py','--static', str(temperature), str(threshold)], stdout=subprocess.PIPE, shell=False)
    return "Friar Tuck is at work. /help"

def main() -> None:

    if not CONFIG["telegram_users"] and not CONFIG["telegram_token"]:
        print("Bad configuration")
        exit()

    updater = Updater(CONFIG["telegram_token"])

    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("status", status_command))
    dispatcher.add_handler(CommandHandler("list", list_command))
    dispatcher.add_handler(CommandHandler("terminate", terminate_command))
    dispatcher.add_handler(CommandHandler("smart", smart_command))
    dispatcher.add_handler(CommandHandler("dsmart", dsmart_command))
    dispatcher.add_handler(CommandHandler("static", static_command))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()