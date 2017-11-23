# -*- coding: utf-8  -*-
import logging

import config
import telebot
import json
#from shortuuid import uuid
import time
from flask import Flask, request, abort
import db
from telebot import types
from log import logger
from session import cookie_session

bot = telebot.TeleBot(config.TOKEN)
app = Flask(__name__)
#app.debug = True

@app.route('/bot', methods=['GET', 'HEAD'])
def webhook():
    bot.remove_webhook()
    bot.set_webhook("https://62.109.13.25:8443/bot",  certificate=open(config.WEBHOOK_SSL_CERT, 'r'))
    return '!'


@app.route('/bot', methods=['POST'])
def send_message():
    logger.info('WEBHOOK: HEADERS:{}  BODY:{}'.format(request.headers, request.data))

    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''

    else:
       logger.error('FAIL HEADERS:{}'.format(request.headers))


def main_menu( txt, id, buttons):
    """
    set inline keyboard
    """
    l_button = []

    for button in buttons:
        l_button.append(types.InlineKeyboardButton (
            text = button.label, callback_data = json.dumps(
                dict( handler=button.handler ))
        ))

    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*l_button)
    bot.send_message(id, txt, reply_markup = keyboard)


@bot.message_handler(commands=['start','help'])
def message_start(message):
    user_markup = None
    #TODO  тут можно добавить дополнительные кнопки
    #user_markup = types.ReplyKeyboardHide()
    #user_markup = types.ReplyKeyboardMarkup(True, True)
    #user_markup.row('/menu')
    content = config.HELP
    bot.send_message(message.chat.id, content, reply_markup = user_markup)


@bot.message_handler(commands=['list'])
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
    bot.send_message(message.chat.id, '<b>Groups</b>', reply_markup=keyboard, parse_mode='HTML')


#TODO тут доделать
@bot.message_handler(commands=['update'])
def service_command_update(message):
    if config.SECRET_COD in message.text:
        db.update_db()
        bot.send_message(message.chat.id, 'Done.')
        logger.debug('Update')


#TODO работает
@bot.message_handler(commands=['last'])
def send_last_posts(message):
    #default value
    str_range = map(str, range(1,6)) # '1','2'...'5'
    l_str_cnt = filter( lambda x: x in message.text, str_range)
    cnt = int(l_str_cnt[0]) if l_str_cnt else 3

    last_posts = db.get_last_posts(cnt)
    cookie_uuid = cookie_session.id
    cookie_session.add(cookie_uuid, dict(action=['POST EXPAND', 'INFO']))
    for post in last_posts:
        created_at = time.strftime("%H:%M %d-%b-%Y",time.localtime(post.date))
        group = post.group.name
        keyboard = types.InlineKeyboardMarkup(row_width=3)
        callable_button = types.InlineKeyboardButton(text='Expand', callback_data=json.dumps(dict(id =cookie_uuid, button=post.id , cmd=0)))
        #description_button = types.InlineKeyboardButton(text='Info', callback_data=json.dumps(dict(id = cookie_uuid, button = post.id, cmd=1)))
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
    group = post.group.title
    url = 'http://vk.com/{url}'.format(url=post.group.url)

    if post.photos and len(post.text) < 3000:
        text = u'<b>{group}</b>  <code>{time}</code>\n{photo}\n{text}'.format(time=created_at, url=url, group=group, text=post.text, photo=post.photos)
    else:
        text = u'<b>{group}</b>  <code>{time}</code>\n{text}'.format(time=created_at, group=group, text=post.text[:1000])

    #text = post.text[:100] #TODO For debug
    bot.edit_message_text(chat_id=id, message_id=mid, text=text, reply_markup=keyboard, parse_mode="HTML")


@bot.message_handler(commands=['info'])
def view_info(message):
    name = message.text.split(' ')
    if len(name) == 2:
        group = db.get_describe_group(name[1])
        if group:
           text = "<strong>{name}</strong>\n <strong>tel: {phone}</strong>\n {description}\n {photo}".format(name=group.name.encode('utf-8'),
           description=group.description.encode('utf-8'), photo=group.photo, phone=group.phone)
           bot.send_message(message.chat.id, text , parse_mode= 'HTML')


def send_expanded_post(call, post_id):
    keyboard = None
    post = db.get_post_extand(post_id)
    send(call, post, keyboard)


def send_info(call, post_id):
    post  = db.get_post_extand(post_id)
    group = db.get_describe_group(post.group.title)

    logger.debug('{} {} {}'.format(post_id, post,  group))
    if group:
        text = "<strong>{name}</strong>\n <strong>tel: {phone}</strong>\n {info}\n {photo}".format(name=group.name.encode('utf-8'),
                                      info=group.description.encode('utf-8'), photo=group.photo, phone=group.phone)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='HTML')

    else:
        logger.error('Info at group')


def choose_next_post(call, sid):

    d_session =  cookie_session.get(sid)
    group_id = int(d_session.get('group'))
    page  = d_session.get('page')
    logger.debug('choose post\tCOOKIE:{}'.format(sid))
    buttons = ['next', 'previous']
    post = db.get_post_from_group(group_id, page)
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keys = list()
    logger.debug('PAGE:{}'.format(page))
    for i in buttons:
        btn = types.InlineKeyboardButton(text = str(i), callback_data = json.dumps(dict(id=sid, button=i.upper())))
        keys.append(btn)

    group = db.get_group(group_id)
    keys.append(types.InlineKeyboardButton(text='Group', url='http://vk.com/%s'%group.url))
    #keys.append(types.InlineKeyboardButton(text='Info', callable_button = json.dumps(dict(id=sid, button=))))
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

            if action == ['POST EXPAND', 'INFO']:
                cmd = dict_callback.get('cmd')
                post_id = callback_button

                if cmd == 0:
                    send_expanded_post(call, post_id)

                elif cmd ==1:
                    send_info(call, post_id)

            elif action == 'GROUP DETAIL':
                ID_GROUPS_ALL = [i.id for i in db.get_all_group()]
                page = data_for_session.get('page', 0)
                group_id = None

                if callback_button == 'PREVIOUS':
                    page += 1 if page is not 30 else 0
                    group_id = data_for_session.get('group')

                elif callback_button == 'NEXT':
                    page -= 1 if page is not 0 else 0
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
    app.run(
        host = '127.0.0.1',
        port = 5000,
        debug=config.DEBUG,

     )
