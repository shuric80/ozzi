#-*- coding: utf-8  -*-


import logging
import config
import telebot
import json
from shortuuid import uuid

from telebot import types
from sqlalchemy.orm import sessionmaker

from models import  engine
from models import EventMenu, Group, Tag, Post

import db

cnt = 1

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


    
class Session:
    def __init__(self):
        self._d = dict()

    @property
    def id(self):
        return uuid()

    def add(self,id, d_input):
        assert(type(d_input == 'dict'))
        self._d[id] = d_input

    def get(self, id):
        return self._d.get(id)

    @property
    def debug(self):
        return self._d

    

pagination = Pagination()  
            
session = Session()

@bot.message_handler(commands=['start','help'])
def message_start_help(message):
    content = '*Это бот для агрегации новостей по теме социальных танцев, \
    новости выбираются соотвествующим тегом'
   
    bot.send_message(message.chat.id, content)

    
@bot.message_handler(func=lambda message:True, content_types=['text'])
def main(message):
    menu = db.mainKeyboard()
    keyboard = types.InlineKeyboardMarkup(row_width=4)
    l_btns = list()
    for btn in menu:
        callable_button = types.InlineKeyboardButton(text=btn.group, callback_data= json.dumps(dict(button=btn.group)))
        l_btns.append(callable_button)

    keyboard.add(*l_btns)
    bot.send_message(message.chat.id, 'main menu', reply_markup=keyboard)

    

def send(id, post, buttons, session_id):
    """ Send post
       """
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keys = list()
    for i in buttons:
        btn = types.InlineKeyboardButton( text = str(i), callback_data = json.dumps(dict(id=session_id, button=str(i))))
        keys.append(btn)

    post.photo = 'http://placehold.it/300x150'
    keyboard.add(*keys)
    bot.send_photo(chat_id = id, photo= post.photo, \
                        caption= post.content, reply_markup = keyboard)

        
def sendDiredPost(call, sid):
    d_session =  session.get(sid)
    assert(d_session)
    group = d_session.get('group')
    page  = d_session.get('page')
    buttons = ['back', 'forward', 'cancel']
    post = db.postInGroup(group, page)
    if post:
        send(call.message.chat.id, post, buttons, sid)
    else:
        logger.debug('Post no found:')
    

        
@bot.callback_query_handler(func=lambda call:True)
def callback_data(call):
     """ callback button
       """
     if call.message:
        event =json.loads(call.data).get('button')
        assert(event)
        q_groups = db.groupAll()
        groups = [i.group for i in q_groups]
        if event in groups:
            sid = session.id
            session.add(sid, dict(page=0, group=event))
            sendDiredPost(call, sid)

        elif event in ['back','cancel','forward']:
            sid  = json.loads(call.data).get('id')
            assert(sid)
            d_session = session.get(sid)
            if  not d_session:
                return
            group = d_session.get('group')
            page = d_session.get('page')
         

            if event == 'forward':
                page += 1
            elif event == 'back':
                page -= 1
            else:
                page = 0
            session.add(sid, dict(page=page, group=group))
            logger.debug(session.debug)
            sendDiredPost(call, sid)

        else:
            logger.debug(call.data)
            



if __name__ =='__main__':
   bot.polling(none_stop=True)
