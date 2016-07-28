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


@bot.message_handler(commands=['start', 'tag', 'group','event'])
def message_start_event(message):
    content = dict()
    content = dict(MAIN = 'This bot for news')
    content = dict(TAG = 'Choose one tag')
    content = dict(GROUP = 'Chose name group')
    

    list_btn = list()
    if message.text == '/start':
        menu = db.getMainButton()
        content = content['MAIN']
        
    elif message.text == '/tag':
        menu = db.getTagsButton()
        content = content['TAG']

    elif message.text == '/group':
        menu = db.getGroupsButton()
        content = content['GROUP']

    elif message.text == '/last':
        pass
        #menu = db.getLastPost()
        
    else:
        bot.reply_to('It is command not use.')

    _l_btn =list()    
    for btn in menu:
        _l_btn.append( types.InlineKeyboardButton(
            text = btn.label,  callback_data = json.dumps(dict(
                event = btn.label, page = 0 ) ))
        )

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*l_btn)
    bot.send_message(message.chat.id , content, reply_markup = keyboard)


    
@bot.callback_query_handler(func = lambda call: True)
def callback_data(call):
    """ callback function bu ttons
       """

    if call.message:
        logger.debug(call.data)
        
        try:
            d_input = json.loads(call.data)

        except ValueError,e:
            d_input = {}
            logger.error(e)

        id = call.message.chat.id

        event =  d_input.get('event', None)
        direction = d_input.get('direction', None)

        menu = db.getTagsObject()

        if id_tag in [i.id for i in menu]:

            if direction in [u'back', u'next']:

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
                        dict( id_tag = id_tag, cnt_page = page, direction = str(i) ))
                )
                list_btns.append(btn)

            keyboard.add(*list_btns)
            
            d_input = dict(id_tag = id_tag, cnt_page=page)
            p = db.getContent(d_input)
            if p:
                content = p.content[:4000]
                photo_path = ('/').join(('static', p.photo_path))

                if os.path.exists(photo_path):
                    photo = open(photo_path,'rb')
                    bot.send_photo(id, photo)

                bot.send_message(id, content, reply_markup = keyboard)




if __name__ =='__main__':
    bot.polling(none_stop=True)
