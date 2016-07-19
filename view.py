#-*- coding: utf-8  -*-

import logging
import config
import telebot

import json

from telebot import types
from sqlalchemy.orm import sessionmaker

from models import  engine
from models import MainMenu, Group, Tag, Post

import db

from handlers import callback_handler
from session import SessionBuffer

logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)

bot  = telebot.TeleBot(config.TOKEN)
callback_handler = dict()

session = SessionBuffer()


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
    
    
@bot.message_handler(regexp='^next$|^back$|^cancel$')
def custom_keyboard_event(message):
    command = message.text
    #tag  = session.cmd(id, command)
    page = 0 
    context ='context'# = db.getTagPost(tag, page)
    photo = open('static/1.jpeg','rb')
    post_send(id, context, photo)

       
@bot.message_handler(func=lambda message:True, content_types=['text'])
def tags_menu(message):
    print ('Tag')
    """  Main menu.  View all tags
      """
    #direct_keyboard()
    #photo = open('static/1.jpeg','rb')
    #post_send(message.chat.id, 'Choose one tag.',photo, tags_menu)


def _error_hook(obj):
    logging.error('Not found handler:%s' % obj )
    
@bot.callback_query_handler(func = lambda call:True)
def callback_data(call):
    """ callback function buttons
       """ 
    if call.message:
        if call.data in db.getTags():
            #session.add(call.message.chat.id, tag, 0)
            #post, photo = db.get_post_tag(call.data, 0)
            post = 'post'
            photo = open('static/1.jpeg','rb')
        elif call.message in callback_handler.keys():
           f_handler = call.message
           callback_handler.get(f_handler, _error_hook)(call)


if __name__ =='__main__':
    bot.polling(none_stop=True)

