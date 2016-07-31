#-*- coding: utf-8  -*-

import os
import logging
import config
import telebot

import json

from telebot import types
from sqlalchemy.orm import sessionmaker

import db

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logger.info('Run view module')

bot  = telebot.TeleBot(config.TOKEN)

def menu(txt, message, buttons):
    """
    set inline keyboard
    """
    l_button = []
    for button in buttons:
        l_button.append( types.InlineKeyboardButton (
            text = button.label, callback_data = button.handler
        ))

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*l_button)
    bot.send_message(message.chat.id, txt, reply_markup = keyboard)


@bot.message_handler(commands=['start', 'tag', 'group','event'])
def message_start_event(message):

    if message.text == '/start':
        l_buttons = db.mainMenu()
        menu('Choose one',message, l_buttons )

    elif message.text == '/tag':
        l_buttons = db.tagMenu()
        menu('Choose tag', message, l_buttons)

    elif message.text == '/group':
        l_buttons = db.groupMenu()
        menu('Choose group', message, l_buttons)

    elif message.text == '/event':
        l_buttons = db.eventMenu()
        menu('Choose event', message, l_buttons)

    else:
        pass


@bot.callback_query_handler(func = lambda call: True)
def callback_data(call):
    """ callback function bu ttons
       """
    if call.message:
        handler = call.data.upper()
        logger.debug('HANDLER:%s' % handler)
        """
        if handler not in state.keys():
            raise 'Handler not find for state'

        msg, ret_event = state[handler]

        if ret_event:
            menu(msg, ret_event)
        """



if __name__ =='__main__':
    bot.polling(none_stop=True)
