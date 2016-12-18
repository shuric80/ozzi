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
    telebot.logger.setLevel(logging.DEBUG)

else:    
    telebot.logger.setLevel(logging.WARNING)


logger = telebot.logger
bot  = telebot.TeleBot(config.TOKEN)


class Session:
    instance = None
    #create singleton
    def __new__(cls):
        if cls.inctance is None:
            cls = super(C, cls).__new__(cls)

        return cls.instance

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

text = """<strong>Этот бот  новостей по теме социальных танцев.</strong> 
Он умеет так: 
/groups - меню по всем группам.
/last - 5 последних сообщений.
/about [name] - информация о школе [name].
/news [tag] - новости по тэгу [tag]
/help - вывод этого меню.
    """


@bot.message_handler(commands=['start','help'])
def message_start(message):
    bot.send_message(message.chat.id, text, parse_mode='HTML')

@bot.message_handler(commands=['groups'])
def main(message):
    menu = db.groupAll()
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    l_btns = list()
    for btn in menu:
        callable_button = types.InlineKeyboardButton(text=btn.name.split(' ')[0], callback_data= json.dumps(dict(button=btn.id)))
        l_btns.append(callable_button)

    keyboard.add(*l_btns)
    bot.send_message(message.chat.id, 'main menu', reply_markup=keyboard, parse_mode='HTML')

@bot.message_handler(commands='update')
def update(message):
    pass
    
    
@bot.message_handler(commands=['last'])
def last(message):
    cnt = 5
    if len(message.text.split(' ')) >1:
        try:
            cnt = int(message.text.split(' ')[1])  if 0 < cnt< 10 else 5 
        except ValueError:
            cnt = 5

    #assert(cnt >0 and cnt < 30)
    last_posts = db.lastPosts(cnt)
    button = 'Открыть'
    for post in last_posts:
        created_at = time.strftime("%H:%M %d-%b-%Y",time.localtime(post.date))
        group = post.group.name
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        callable_button = types.InlineKeyboardButton(text=button, callback_data=json.dumps(dict(post=post.id)))
        url_button = types.InlineKeyboardButton(text='Group', url='http://vk.com/{url}'.format( url=post.group.url))
        text = u'<code>{time}</code>\n<b>{group}</b>\n{text}...'.format(time=created_at, group=group, text=post.text[:200])
        keyboard.add(callable_button)
        bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='HTML', disable_web_page_preview=True)

        
def send(call, post, keyboard):
    """ Send post
       """
    id = call.message.chat.id
    mid = call.message.message_id
    created_at = time.strftime("%H:%M %d-%b-%Y",time.localtime(post.date))
    group = post.group.name
    url = 'http://vk.com/{url}'.format(url=post.group.url)
    
    if post.photos and len(post.text) < 3000:
        text = u'<code>{time}</code>\n<b>{group}</b>\n{photo}\n{text}'.format(time=created_at, url=url, group=group, text=post.text, photo=post.photos)
    else:
        text = u'<code>{time}</code>\n<b>{group}</b>\n{text}'.format(time=created_at, group=group, text=post.text[:4000])

    bot.edit_message_text(chat_id=id, message_id=mid, text=text, reply_markup=keyboard, parse_mode="HTML")
    #bot.edit_message_text(chat_id=id,message_id=mid,text='%s \n%s'%(post.photos, post.text), reply_markup=keyboard)

    
def sendPost(call, post_id):
    keyboard=None
    post = db.getPost(post_id)
    send(call, post, keyboard)
    

def sendDiredPost(call, sid):
    d_session =  session.get(sid)
    assert(d_session)
    group_id = d_session.get('group_id')
    page  = d_session.get('page')
    buttons = ['back', 'forward']
    post = db.postInGroup(group_id, page)
    if not post:
        return
    assert(post)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keys = list()

    #menu_markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard= True)
    #menu_markup.row('/menu')

    for i in buttons:
        btn = types.InlineKeyboardButton(text = str(i), callback_data = json.dumps(dict(id=sid, button=str(i))))
        keys.append(btn)
    group = db.groupID(group_id)
    keys.append(types.InlineKeyboardButton(text='Goto to group', url='http://vk.com/%s'%group.url))
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
        post_id = json.loads(call.data).get('post')

        if post_id:
            sendPost(call, post_id)
            return
        
        assert(event)
        groups_all = db.groupAll()
        assert(groups_all)
        groups_id = [i.id for i in groups_all]
        if event in groups_id:
            logger.debug('choosed group:%s' % event)
            sid = session.id
            session.add(sid, dict(page=0, group_id=event))
            sendDiredPost(call, sid)

        elif event in ['back','forward']:
            sid  = json.loads(call.data).get('id')
            assert(sid)
            d_session = session.get(sid)
            if  not d_session:
                return
            group_id = d_session.get('group_id')
            page = d_session.get('page')

            if event == 'forward':
                page += 1

            elif event == 'back':
                page -= 1

            else:
                page = 0

            session.add(sid, dict(page=page, group_id=group_id))
            logger.debug(session.debug)
            sendDiredPost(call, sid)

        else:
            logger.debug(call.data)

            
if __name__ =='__main__':
    bot.polling(none_stop=True)
