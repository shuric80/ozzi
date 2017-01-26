#-*- coding: utf-8  -*-

import logging
import config
import telebot
import json
from shortuuid import uuid
import time

from telebot import types

from models import  engine
from models import Group, Post
import db

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logger.info('Run view module')

bot  = telebot.TeleBot(config.TOKEN)


def main_menu(txt, id, buttons):
    """
    set inline keyboard
    """
    l_button = []

    for button in buttons:
        l_button.append( types.InlineKeyboardButton (
            text = button.label, callback_data = json.dumps(
                dict( handler=button.handler ))
        ))

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*l_button)
    bot.send_message(id, txt, reply_markup = keyboard)

        
class Session:
    #create session
    instance = None

    def __new__(cls):
        if cls.instance is None:
            cls = super(C, cls).__new__(cls)

        return cls.instance

    @property
    def id(self):
        return uuid()

    def add(self,id, d_input):
        if isinstanse(d_input, dict):
            self._d[id] = d_input

    def get(self, id):
        return self._d.get(id)

    @property
    def debug(self):
        return self._d


session = Session()


@bot.message_handler(commands=['start','help'])
def message_start(message):
    user_markup = None
    #TODO  тут можно добавить дополнительные кнопки
    #user_markup = types.ReplyKeyboardHide()
    #user_markup = types.ReplyKeyboardMarkup(True, True)
    #user_markup.row('/menu')
    content = config.HELP
    bot.send_message(message.chat.id, content, reply_markup=user_markup)
 
    
@bot.message_handler(commands='update')
def service_command_update(message):
    secret_cod = "ku"
    if secret_cod in message:
        db.update_db()
        bot.send_message(message.chat.id, 'Done.')
        logger.debug('Update')
    
#TODO тут не работает    
@bot.message_handler(commands=['last'])
def send_lasttime_posts(message):
    cnt = 5 #default value  
    str_range = map(str, range(1,6)) # '1','2'...'5'
    l_str_cnt = filter( lambda x: x in message.text, str_range)
    if l_str_cnt:
        cnt = int(l_str_cnt[0])
        
    last_posts = db.get_last_posts(cnt)
    
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
    created_at = time.strftime("%H:%M %d-%b",time.localtime(post.date))
    group = post.group.name
    url = 'http://vk.com/{url}'.format(url=post.group.url)
    
    if post.photos and len(post.text) < 3000:
        text = u'<b>{group}</b>  <code>{time}</code>\n{photo}\n{text}'.format(time=created_at, url=url, group=group, text=post.text, photo=post.photos)
    else:
        text = u'<b>{group}</b>  <code>{time}</code>\n{text}'.format(time=created_at, group=group, text=post.text[:4000])

    bot.edit_message_text(chat_id=id, message_id=mid, text=text, reply_markup=keyboard, parse_mode="HTML")
    #bot.edit_message_text(chat_id=id,message_id=mid,text='%s \n%s'%(post.photos, post.text), reply_markup=keyboard)


"""
@bot.message_handler(commands='description')
def view_description(message):
    
    user_name = message.text.
 
    group = db.about(name)
    if group:
        text = "{name}\n{photo}\n{phone}\n{description}".format(name=group.name,
                                                          description=group.description,
                                                          phone=group.phone,
        photo = group.photo)
        bot.send_message(message.chat.id, text)
    
  """

def send_post(call, post_id):
    keyboard=None
    post = db.get_post_extand(post_id)
    send(call, post, keyboard)
    

def choose_next_post(call, sid):
    
    d_session =  session.get(sid)
    assert(d_session)
    group_id = d_session.get('group_id')
    page  = d_session.get('page')
    buttons = ['back', 'forward']
    post = db.postInGroup(group_id, page)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keys = list()

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
        assert(event)
        q_groups = db.groupAll()
        groups_id = [i.id for i in q_groups]

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
