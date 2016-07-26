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
handler = logging.FileHandler('../log/tbot.log')

logger.addHandler(handler)

bot  = telebot.TeleBot(config.TOKEN)



@bot.message_handler(commands=['start','help'])
def message_start_help(message):
    content_ru = "*Это бот для агрегации новостей по теме социальных танцев, \
    новости выбираются соотвествующим тегом."
    content_en = 'This bot for news'

    list_btn = list()
    #menu = db.getMainButton()
    menu = db.getTagsIdTag()
    for btn in menu:
        btn_event = types.InlineKeyboardButton(
            text= u'%s' % btn.label,  callback_data = json.dumps(dict(
                label = u'%s' %btn.label, cnt_page=0) ))

        list_btn.append(btn_event)

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*list_btn)
    bot.send_message(message.chat.id , content_en, reply_markup = keyboard)


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


        label =  d_input.get('label', None)
        direction = d_input.get('direction', None)

        menu = db.getMainButton()

        if label in [i.label for i in menu]:

            if direction in [u'back',u'next']:

               if d_input[u'direction'] == u'next':
                   d_input[u'cnt_page'] += 1 if d_input[u'cnt_page'] <10 else 0

               elif d_input[u'direction'] == u'back':
                   d_input[u'cnt_page'] -= 1 if d_input[u'cnt_page'] > 0 else 0

               logging.debug('Step:%s' % d_input[u'cnt_page'])

               if d_input[u'cnt_page'] == 0 or d_input[u'cnt_page'] ==10:
                   return

            else:
                d_input[u'cnt_page'] = 0


            keyboard = types.InlineKeyboardMarkup(row_width=2)
            list_btns = list()
            page = d_input['cnt_page']

            for i in [u'back',u'next',u'cancel']:
                btn = types.InlineKeyboardButton(
                    text=str(i), callback_data= json.dumps(
                        dict( label = label, cnt_page = page, direction = str(i) ))
                )
                list_btns.append(btn)

            keyboard.add(*list_btns)

            db_data = db.getContent(tag, page)
            #if not db_data:
            #    return
            #db_data = ['static/a0F58mqrUhg.jpg', 'content']
            content = db_data[1]
            photo_path = db_data[0]
            print photo_path

            if os.path.exists(photo_path):
                photo = open(photo_path,'rb')
                bot.send_photo(id, photo, caption=content,reply_markup = keyboard)

            else:
                bot.send_message(id, content, reply_markup = keyboard)




if __name__ =='__main__':
    bot.polling(none_stop=True)
