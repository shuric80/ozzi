#-*- coding: utf-8  -*-

import logging
import config
import telebot
import json
from shortuuid import uuid
import time

from telebot import types

from models import Group, Post

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)
logger.info('Run view module')

bot  = telebot.TeleBot(config.TOKEN)

import db


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
    __instance = None
    def __new__(cls, val):
        if  Session.__instance is None:
            Session.__instance = object.__new__(cls)

        Session.__instance.val = val
        return Session.__instance

    
    def __init__(self):
        self._d = dict()

    @property
    def id(self):
        return uuid()

    def add(self,id, d_input):
        #if isinstance(d_input, dict) and isinstance(id, str):
        logger.debug('Session add: {id} : {data}'.format(id=id, data=d_input))
        self._d[id] = d_input

    def get(self, id):
        return self._d.get(id)
    
    def __repr__(self):
        return '<>'.format(self._d)


cookie_session = Session()


@bot.message_handler(commands=['start','help'])
def message_start(message):
    user_markup = None
    #TODO  тут можно добавить дополнительные кнопки
    #user_markup = types.ReplyKeyboardHide()
    #user_markup = types.ReplyKeyboardMarkup(True, True)
    #user_markup.row('/menu')
    content = config.HELP
    bot.send_message(message.chat.id, content, reply_markup = user_markup)


@bot.message_handler(commands=['groups'])
def view_list_groups(message):
    all_group_list =  db.get_all_group()
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    l_btns = list()
    uuid_cookie = cookie_session.id
    for btn in all_group_list:
        callable_button = types.InlineKeyboardButton(text=btn.title, callback_data= json.dumps(dict(id = uuid_cookie, button=btn.id)))
        l_btns.append(callable_button)

    keyboard.add(*l_btns)
    cookie_session.add(uuid_cookie, dict(action='GROUP DETAIL'))
    bot.send_message(message.chat.id, 'List group', reply_markup=keyboard, parse_mode='HTML')
    
    
@bot.message_handler(commands='update')
def service_command_update(message):
    secret_cod = "ku"
    if secret_cod in message:
        db.update_db()
        bot.send_message(message.chat.id, 'Done.')
        logger.debug('Update')
    
#TODO работает    
@bot.message_handler(commands=['last'])
def send_lasttime_posts(message):
    #default value  
    str_range = map(str, range(1,6)) # '1','2'...'5'
    l_str_cnt = filter( lambda x: x in message.text, str_range)
    cnt = int(l_str_cnt[0]) if l_str_cnt else 5
        
    last_posts = db.get_last_posts(cnt)
    cookie_uuid = cookie_session.id
    cookie_session.add(cookie_uuid, dict(action='POST EXPAND'))
    button = 'Открыть'
    for post in last_posts:
        created_at = time.strftime("%H:%M %d-%b-%Y",time.localtime(post.date))
        group = post.group.name
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        callable_button = types.InlineKeyboardButton(text=button, callback_data=json.dumps(dict(id =cookie_uuid, button=post.id)))
        url_button = types.InlineKeyboardButton(text='Group', url='http://vk.com/{url}'.format( url=post.group.url))
        text = u'<code>{time}</code>\n<b>{group}</b>\n{text}...'.format(time=created_at, group=group, text=post.text[:200])
        keyboard.add(callable_button)
        bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='HTML', disable_web_page_preview=True)

        
def send(call, post, keyboard):
    """ Send post
       """
    logger.debug('SEND')
    id = call.message.chat.id
    mid = call.message.message_id
    created_at = time.strftime("%H:%M %d-%b",time.localtime(post.date))
    group = post.group.title
    url = 'http://vk.com/{url}'.format(url=post.group.url)
    
    if post.photos and len(post.text) < 3000:
        text = u'<b>{group}</b>  <code>{time}</code>\n{photo}\n{text}'.format(time=created_at, url=url, group=group, text=post.text, photo=post.photos)
    else:
        text = u'<b>{group}</b>  <code>{time}</code>\n{text}'.format(time=created_at, group=group, text=post.text[:1000])

    #text = post.text[:100] #TODO For debug
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

def send_expanded_post(call, post_id):
    keyboard = None
    post = db.get_post_extand(post_id)
    send(call, post, keyboard)

    
#TODO тут чтото с потоками.
def choose_next_post(call, sid):
   
    d_session =  cookie_session.get(sid)
    group_id = int(d_session.get('group'))
    page  = d_session.get('page')
    logger.debug('choose post\tCOOKIE:{}'.format(sid))
    buttons = ['back', 'forward']
    post = db.get_post_from_group(group_id, page)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keys = list()

    for i in buttons:
        btn = types.InlineKeyboardButton(text = str(i), callback_data = json.dumps(dict(id=sid, button=i.upper())))
        keys.append(btn)
 
    group = db.get_group(group_id)
    keys.append(types.InlineKeyboardButton(text='Goto to group', url='http://vk.com/%s'%group.url))
    keyboard.add(*keys)

    if post:
          send(call, post, keyboard)
    else:
        logger.debug('Post no found:')


@bot.callback_query_handler(func=lambda call:True)
def callback_data(call):
    """ callback button
       """
    if call.message:
        dict_callback = json.loads(call.data)
        cookie_uuid = dict_callback.get('id')
        data_for_session = cookie_session.get(cookie_uuid)
        if data_for_session:
            action = data_for_session.get('action')
            callback_button = dict_callback.get('button')
            logger.debug('COOKIE:{}'.format(data_for_session))
            logger.debug('CALLBACK_DATA:{}'.format(callback_button))
 
            if action == 'POST EXPAND':
                logger.debug('EXPAND')
                post_id = callback_button
                send_expanded_post(call, post_id)

            elif action == 'GROUP DETAIL':
                ID_GROUPS_ALL = [i.id for i in db.get_all_group()]
                page = data_for_session.get('page', 0)
                group_id = None
            
                if callback_button == 'FORWARD':
                    page += 1
                    group_id = data_for_session.get('group')

                elif callback_button == 'BACK':
                    page -= 1
                    group_id = data_for_session.get('group')

                elif callback_button in ID_GROUPS_ALL:
                    page = 0
                    group_id = int(callback_button)

                else:
                    logger.debug('ELSE')
                
                new_cookie = dict(group = group_id, page=page, action='GROUP DETAIL')  
                cookie_session.add(cookie_uuid, new_cookie)
                choose_next_post(call, cookie_uuid)
            
        else:
            logger.debug(call.data)


            
if __name__ =='__main__':
    bot.polling(none_stop=True)
    
