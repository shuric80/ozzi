#-*- coding: utf-8  -*-

import logging
import config
import telebot
import util
import json

from telebot import types
from sqlalchemy.orm import sessionmaker

from models import  engine
from models import MainMenu, Group, Tag, Post

import db

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot  = telebot.TeleBot(config.TOKEN)
callback_handler = dict()


class Pagination:
    def __init__(self):
        self.cnt = 0

    def reset(self):
        self.cnt =0

    def inc(self):
        self.cnt += 1 if self.cnt <10 else 0

    def dec(self):
        self.cnt -= 1 if self.cnt > 0 else 0

    @property
    def cnt(self):
        return self.cnt

pagination = Pagination()  

def post_send(id, txt, photo, buttons = None):
    """ Send post
       """
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keys = list()
    if buttons:
        for i in buttons:
            btn = types.InlineKeyboardButton( text= str(i), callback_data = str(i))

        keys.append(btn)
        keyboard.add(*keys)

    bot.send_photo(chat_id = id, photo=photo, \
                        caption= txt, reply_markup = keyboard)

def direct_keyboard():
    buttons  = ('Back','Next','Main') 
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True, row_width=2)
    keyboard.add(*buttons)
    return keyboard


@bot.message_handler(commands=['start','help'])
def message_start_help(message):
    content = '*Это бот для агрегации новостей по теме социальных танцев, \
    новости выбираются соотвествующим тегом'
    
    bot.send_message(message.chat.id, content)
    
    
@bot.message_handler(func=lambda message:True, content_types=['text'])
def tags_menu(message):
    """  Main menu.  View all tags
      """
    tags_menu = db.get_tags()
    post_send(message.chat.id, 'Choose one tag.', buttons = tags_menu)


@bot.message_handler(regexp='^Next$|^Back$|^Main$')
def custom_keyboard_event(message):
    if message.text == 'Next':
        pagination.inc()

    elif message.text == 'Back':
        pagination.dec()

    elif message.text == 'Main':
        pagination.reset()


def test(call):
    logging.info('callback')

callback_handler['test'] = test

    
@bot.callback_query_handler(func=lambda call:True)
def callback_data(call):
    """ callback function buttons
       """ 
    if call.message:
        if call.data in db.get_tags():
            page = pagination.cnt
            post, photo = db.get_post_tag(call.data)
            post_send(id = call.message.chat.id, txt = post, \
                          photo = photo)
            
        elif call.message in callback_handler.keys():
           f_handler = call.message
           callback_handler[f_handler](call)


if __name__ =='__main__':
    bot.polling(none_stop=True)

