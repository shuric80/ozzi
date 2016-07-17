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

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot  = telebot.TeleBot(config.TOKEN)

Session = sessionmaker(bind = engine)
session = Session()

TASK_MENU = [q[0] for q in session.query(MainMenu.menu).all()]
GROUP_MENU = dict(session.query(Group.group, Group.vk_address).all())
 
class Pagination:
    def __init__(self):
        self.cnt = 0

    def add(self):
        self.cnt += 1
        if self.cnt >2:
            self.cnt = 2
        return self.cnt 

    def div(self):
        self.cnt -= 1
        if self.cnt < 0:
            self.cnt = 0
        return self.cnt

pagination = Pagination()  
            
@bot.message_handler(commands=['start','help'])
def message_start_help(message):
       
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    keyboard.add(*TASK_MENU)
    bot.send_message(message.chat.id, u'Choose event..',reply_markup=keyboard)
    
    
@bot.message_handler(func=lambda message:True, content_types=['text'])
def index(message):
    
    if message.text not in TASK_MENU:
        return
    
    keyboard = types.InlineKeyboardMarkup(row_width=2)
  
    menu = GROUP_MENU.keys()
    btn_list = list()
    for i in menu:
        callable_button = types.InlineKeyboardButton(text ='%s'%i , callback_data=str(i))
        btn_list.append(callable_button)

    keyboard.add(*btn_list)
    bot.send_message(message.chat.id, 'choose one...',reply_markup=keyboard)



def post_send(id, txt, photo, buttons):
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
        
    if call.message:
        if call.data in GROUP_MENU.keys():
            photo, post = session.query(Post.photo,Post.post).join(Group.posts). \
                          filter(Group.group == call.data).one()
            
            post_send(id = call.message.chat.id, txt = post, \
                          photo = photo, buttons = ('back','next'))
         
        elif call.data in ['back','next']:
            if call.data == 'back':
                page = pagination.div()
            else:
                page = pagination.add()
                
            photo = open('static/2.jpeg', 'rb')
            post_send(id = call.message.chat.id, txt = 'ne post', \
                      photo = photo, buttons = ('back', 'next'))
          


if __name__ =='__main__':
    bot.polling(none_stop=True)

