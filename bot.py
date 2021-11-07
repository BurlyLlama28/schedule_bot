import datetime
import logging
from sys import stdout
import pytz
import requests
import telegram
from redis import Redis
from requests.api import get
from rq import Queue
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import (CommandHandler, Filters, InlineQueryHandler,
                          MessageHandler, Updater)

updater = Updater(
    token="2115629436:AAHy2wczrznIAwLzyR-CqhRsDATACb4C9zE", use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
CHAT_ID = 0

# basic queue
j = updater.job_queue


def say_payday():
    return "@BLlama28, @yourdrunkfather,\n @I_anbo, @bodya_ka\n\nIt's <b>Payday time!</b>"


# function to handle the /start command
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Konnichiwa, I'm your schedule-bot!\n\nSend /help to see what I can.")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def help_bot(update, context):
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    print(CHAT_ID)
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Arigatogozaimasu! You helped me to identify your chat")


help_bot_handler = CommandHandler('help_bot', help_bot)
dispatcher.add_handler(help_bot_handler)


def monthly(context):
    global CHAT_ID
    print(CHAT_ID)
    # send message to all users
    context.bot.send_message(
        chat_id=CHAT_ID, text=say_payday(), parse_mode=telegram.ParseMode.HTML)


# function to handle the /start_schedule command
def start_schedule(update, context, ):
    # command = ' '.join(context.args)
    print(datetime.datetime.now())
    jstOffset = datetime.timedelta(hours=2)
    jst = datetime.timezone(jstOffset, "Ukraine Standard Time")
    j.run_monthly(monthly, when=datetime.time(hour=9, minute=0, tzinfo=pytz.timezone("Europe/Kiev")), day=1, name="payday")
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Okay, schedule message turned on")


schedule_on_handler = CommandHandler('start_schedule', start_schedule)
dispatcher.add_handler(schedule_on_handler)


# function to handle the /end_schedule command
def end_schedule(update, context, ):
    for job in j.get_jobs_by_name('payday'):
        job.schedule_removal()
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="Okay, schedule message turned off")


schedule_off_handler = CommandHandler('end_schedule', end_schedule)
dispatcher.add_handler(schedule_off_handler)


# function to handle the /help command
def help(update, context):
    update.message.reply_text(
        'So, I have this commands:\n/help_bot - main command to work with chats\n/start_schedule - turn on schedule message\n/end_schedule - turn off schedule message')


help_handler = CommandHandler('help', help)
dispatcher.add_handler(help_handler)


# function to handle errors occured in the dispatcher
def error(update, context):
    update.message.reply_text('Sorry, an error occured')


def main():
    # start your shiny new bot
    updater.start_polling()

    # run the bot until Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
