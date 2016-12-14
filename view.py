#-*- coding: utf-8  -*-


import logging
import config
import telebot
import json
from shortuuid import uuid
import time

from telebot import types
from sqlalchemy.orm import sessionmaker

from models import  engine
from models import EventMenu, Group, Tag, Post

import db

if config.DEBUG:
    import sys
    sys.dont_write_bytecode = True


logger = telebot.logger
telebot.logger.setLevel(logging.WARNING)

bot  = telebot.TeleBot(config.TOKEN)

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

session = Session()

@bot.message_handler(commands=['start','help'])
def message_start_help(message):
    content = '*Это бот для агрегации новостей по теме социальных танцев, \
    новости выбираются соотвествующим тегом'

    bot.send_message(message.chat.id, content)


@bot.message_handler(func=lambda message:True, content_types=['text'])
def main(message):
    menu = db.mainKeyboard()
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    l_btns = list()
    for btn in menu:
        callable_button = types.InlineKeyboardButton(text=btn.group, callback_data= json.dumps(dict(button=btn.group)))
        l_btns.append(callable_button)

    keyboard.add(*l_btns)
    #bot.reply_to(message,"asad")
    bot.send_message(message.chat.id, 'main menu', reply_markup=keyboard)




def send(call, post, keyboard):
    """ Send post
       """
    id = call.message.chat.id
    mid = call.message.message_id
    created_at = time.strftime("%H:%M %d.%m\n",time.localtime(post.created_at))
    text = '{time}\n{photo}\n{text}'.format(time=created_at,  text=post.content,photo=post.photo)
    bot.edit_message_text(chat_id=id, message_id=mid,text=text, reply_markup=keyboard)
    #bot.send_message(id, '%s \n%s'%(post.photo, post.content), reply_markup=keyboard)



def sendDiredPost(call, sid):
    d_session =  session.get(sid)
    assert(d_session)
    group = d_session.get('group')
    page  = d_session.get('page')
    buttons = ['back', 'forward', 'cancel']
    post = db.postInGroup(group, page)
    post.photo = post.photo if post.photo else ''

    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keys = list()
    for i in buttons:
        btn = types.InlineKeyboardButton( text = str(i), callback_data = json.dumps(dict(id=sid, button=str(i))))
        keys.append(btn)

    keyboard.add(*keys)

    if post:
        send(call, post,keyboard)

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
