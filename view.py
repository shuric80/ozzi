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
telebot.logger.setLevel(logging.ERROR)
logger.info('Run view module')

bot  = telebot.TeleBot(config.TOKEN)

def menu(txt, id, buttons , prefix = None):
    """
    set inline keyboard
    """
    l_button = []

    for button in buttons:
        l_button.append( types.InlineKeyboardButton (
            text = button.label, callback_data =  ('.').join((prefix, button.handler, 0 , '')) if prefix else button.handler
        ))

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*l_button)
    bot.send_message(id, txt, reply_markup = keyboard)


def print_content(id, post, prefix_handler):
    if not post:
        bot.send_message(id, 'nothing')

    else:
        buttons = ['BACK', 'NEXT','CANCEL']
        l_buttons = list()
        for button in buttons:
            handler = ('.').join([prefix_handler, button]).upper()
            l_buttons.append( types.InlineKeyboardButton(
                text = button, callback_data = handler ))

        keyboard = types.InlineKeyboardMarkup(row_width = 2)
        keyboard.add(*l_buttons)

        if post.photo:
            path_photo = '/'.join(('static',post.photo))
            photo = open(path_photo, 'rb')
            bot.send_photo(id, photo,  reply_markup = keyboard)

        else:
            bot.send_message(id, 'post', reply_markup = keyboard)


def group(message, page, ext = None):
    logger.debug('STATE:GROUP:EXT:%s' % ext)
    if not ext:
        groups =  db.groupMenu()
        menu('Group', message.chat.id, groups, 'GROUP')

    else:
        group, page, direct = ext.split('.')
        if direct == 'BACK':
            page -= 1 if page > 0 else 0

        elif direct == 'NEXT':
            page += 1 if page < 10 else 10

        else:
            page = 0

        post = db.readGroup(group, page)
        logger.debug('POST:%s' % post)
        prefix_handler = '.'.join([group,page])

        print_content(message.chat.id, post, prefix_handler)


def tag(message, ext = None):
    logger.debug('STATE:TAG')
    tags = db.tagMenu()
    menu('Tags', message, tags)


def event(message, ext = None):
    logger.debug('STATE:EVENT')
    event = db.eventMenu()
    menu('Event', message, event)


class StateMachine:

    def __init__(self):
        self._state = dict(GROUP = group,
                           TAG = tag,
                           EVENT = event
        )

    def set(self, handler, message):

        _handler = handler
        ext = None


        if '.' in handler:
            _handler, name, page, direct = handler.split('.')


        if _handler not in self._state.keys():
            logger.error('Error: No find handler: %s' % _handler)
            return

        self._state[_handler](message, ext)


stm  = StateMachine()


@bot.message_handler(commands=['start', 'tag', 'group','event'])
def message_start_event(message):

    if message.text == '/start':
        l_buttons = db.mainMenu()
        print l_buttons
        menu('Choose one',message.chat.id, l_buttons )

    elif message.text == '/tag':
        l_buttons = db.tagMenu()
        menu('Choose tag', message.chat.id, l_buttons)

    elif message.text == '/group':
        l_buttons = db.groupMenu()
        menu('Choose group', message.chat.id, l_buttons)

    elif message.text == '/event':
        l_buttons = db.eventMenu()
        menu('Choose event', message.chat.id, l_buttons)

    else:
        pass


@bot.callback_query_handler(func = lambda call: True)
def callback_data(call):
    """ callback function bu ttons
       """
    #if call.message in ['BACK','NEXT','CANCEL']:
    logger.info('DIRECT: %s' % call.message)

    if call.message:

        handler = call.data

        stm.set(handler, call.message)




if __name__ =='__main__':
    bot.polling(none_stop=True)
