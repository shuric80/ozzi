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
telebot.logger.setLevel(logging.INFO)

bot  = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start','help'])
def message_start_help(message):
    content = "*Это бот для агрегации новостей по теме социальных танцев, \
    новости выбираются соотвествующим тегом."

    tags_btn_list =db.getTags()
    list_btn = list()

    for i in tags_btn_list:
        btn = types.InlineKeyboardButton(
            text=str(i), callback_data = json.dumps(dict( tag = i,page=0) ))

        list_btn.append(btn)

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*list_btn)
    bot.send_message(message.chat.id , content, reply_markup = keyboard)


def _error_hook(obj):
    logging.error('Not found handler:%s' % obj )

@bot.callback_query_handler(func = lambda call: True)
def callback_data(call):
    """ callback function bu ttons
       """

    if call.message:
        try:
            d_input = json.loads(call.data)
        except ValueError,e:
            logging.error(e)

        id = call.message.chat.id

        tag =  d_input.get('tag', None)
        direction = d_input.get('direction', None)

        tags = db.getTags()
        if tag in tags:
           if direction in [u'back',u'next']:

               if d_input[u'direction'] == u'next':
                   d_input[u'page'] += 1 if d_input[u'page'] <10 else 0

               elif d_input[u'direction'] == u'back':
                    d_input[u'page'] -= 1 if d_input[u'page'] > 0 else 0

               logging.debug('Step:%s' % d_input[u'page'])

               if d_input[u'page'] == 0 or d_input[u'page'] ==10:
                   print d_input[u'page']
                   return
           else:
               d_input[u'page'] = 0
           print d_input
           keyboard = types.InlineKeyboardMarkup(row_width=2)
           list_btns = list()
           page = d_input['page']
           for i in [u'back',u'next',u'cancel']:
               btn = types.InlineKeyboardButton(
                   text=str(i), callback_data= json.dumps(
                       dict( tag = tag, page = page, direction = str(i) ))
               )
               list_btns.append(btn)

           keyboard.add(*list_btns)

           db_data = db.getContent(tag, page)
           if not db_data:
               return

           content = db_data[1]
           photo_path =db_data[0]

           if os.path.exists(photo_path):
               photo = open(photo_path,'rb')
               bot.send_photo(id, photo, caption=content,reply_markup = keyboard)

           else:
               bot.send_message(id, content, reply_markup = keyboard)





if __name__ =='__main__':
    bot.polling(none_stop=True)

