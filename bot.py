from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import pandas as pd
import logging
import random

from myData import *

# i honestly dont know what this does but im gonna keep it because i dont want to break it
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.ERROR)

def send_greeting(update, context):
  word = random.choice(salutations) + ' ' + random.choice(names+nicknames)
  chat_id = update.message.chat_id
  context.bot.send_message(chat_id=chat_id, text=word)
  context.bot.send_message(chat_id=chat_id, text="remember you can view the list of commands with /help")

def shouldi(update, context):
  chat_id = update.message.chat_id
  context.bot.send_message(chat_id=chat_id, text=random.choice(options))

def pick_timer(update, context):
  chat_id = update.message.chat_id
  context.bot.send_message(chat_id=chat_id, text=str(random.randrange(20, 60, 10)) + " minutes")
  context.bot.send_message(chat_id=chat_id, text="when youre done, do /finished")

def send_image(update, context):
  chat_id = update.message.chat_id
  context.bot.send_photo(chat_id=chat_id, photo= random.choice(images_list))

def messages(update, context): 
  chat_id = update.message.chat_id
  context.bot.send_message(chat_id=chat_id, text=random.choice(facts))

def finish(update: Update, context: CallbackContext) -> None:
  keyboard = [
    [
      InlineKeyboardButton("yes", callback_data='positive'),
      InlineKeyboardButton("no", callback_data='negative'),
    ]
  ]

  reply_markup = InlineKeyboardMarkup(keyboard)

  text = "were you able to finish the timer " + random.choice(nicknames) + "?"
  update.message.reply_text(text, reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
  query = update.callback_query
  query.answer()
  if (query.data == 'positive'):
    query.edit_message_text(text=random.choice(positive))
  else:
    query.edit_message_text(text=random.choice(negative))

def show_commands(update, context):
  chat_id = update.message.chat_id
  context.bot.send_message(chat_id=chat_id, text=commands_list, parse_mode="Markdown")

def main():
  
  # Initiate the bot and add command handler  
  updater = Updater('#YOUR TOKEN#', use_context=True)
  updater.dispatcher.add_handler(CommandHandler('start', send_greeting))
  updater.dispatcher.add_handler(CommandHandler('help', show_commands))
  updater.dispatcher.add_handler(CommandHandler('shouldi', shouldi))
  updater.dispatcher.add_handler(CommandHandler('timer', pick_timer))
  updater.dispatcher.add_handler(CommandHandler('image', send_image))
  updater.dispatcher.add_handler(CommandHandler('text', messages))

  updater.dispatcher.add_handler(CommandHandler('finished', finish))
  updater.dispatcher.add_handler(CallbackQueryHandler(button))

  print("starting bot...")

  # Run the bot
  updater.start_polling()
  updater.idle()
  
if __name__ == '__main__':
  main()
