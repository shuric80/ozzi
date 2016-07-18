#-*- coding: utf-8  -*-


import logging
import config
import telebot
import json

from telebot import types
from sqlalchemy.orm import sessionmaker

from models import  engine
from models import EventMenu, Group, Tag, Post

import db

if config.DEBUG:
    import sys
    sys.dont_write_bytecode = True


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

bot  = telebot.TeleBot(config.TOKEN)

 
class Pagination:
    def __init__(self):
        self.cnt = 0

    def inc(self):
        self.cnt += 1 if self.cnt <10 else 0

    def dec(self):
        self.cnt -= 1 if self.cnt > 0 else 0

    @property
    def cnt(self):
        return self.cnt
        
        


pagination = Pagination()  
            
@bot.message_handler(commands=['start','help'])
def message_start_help(message):
    content = '*Это бот для агрегации новостей по теме социальных танцев, \
    новости выбираются соотвествующим тегом'
   
    bot.send_message(message.chat.id, content)
    
    
@bot.message_handler(func=lambda message:True, content_types=['text'])
def tags_menu(message):
    """  Main menu.  View all tags
      """
    menu = db.get_tags()
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    btn_list = list()
    for i in menu:
        callable_button = types.InlineKeyboardButton(text ='%s'%i , callback_data=str(i))
        btn_list.append(callable_button)

    keyboard.add(*btn_list)
    bot.send_message(message.chat.id, 'Choose one tag.',reply_markup=keyboard)



def post_send(id, txt, photo, buttons):
    """ Send post
       """
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keys = list()
    for i in buttons:
        btn = types.InlineKeyboardButton( text= str(i), callback_data = str(i))
        keys.append(btn)

    keyboard.add(*keys)
    bot.send_photo(chat_id = id, photo=photo, \
                        caption= txt, reply_markup = keyboard)
    

@bot.callback_query_handler(func=lambda call:True)
def callback_data(call):
    """ callback button
       """ 
    if call.message:
        if call.data in db.get_tags():

            post, photo = db.get_post_tag(call.data)
            post_send(id = call.message.chat.id, txt = post, \
                          photo = photo, buttons = ('back','next'))
         
        elif call.data in ['back','next']:
            if call.data == 'back':
                pagination.dec()
            else:
                pagination.inc()
                
            post, photo = db.get_post_tag(call.data, pagination = pagination.cnt)
            post_send(id = call.message.chat.id, txt = post, \
                      photo = photo, buttons = ('back', 'next'))
          


if __name__ =='__main__':
    bot.polling(none_stop=True)

