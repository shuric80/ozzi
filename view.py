# -*- coding: utf-8  -*-

import json
import time

import db
from session import UserSessionRedis
from server import bot
from log import logger
from custom_keybords import keyboard_last_posts, keyboard_list_groups, keyboard_next_page
import config

cookie = UserSessionRedis()


@bot.message_handler(commands=['start','help'])
def message_start(message):
    """Main menu. Cmd help or start.
       """
    user_markup = None
    content = config.HELP
    bot.send_message(message.chat.id, content, reply_markup = user_markup)



@bot.message_handler(commands=['settings'])
def message_settings(message):
     group_list = db.get_all_group()
     sid = cookie.id
     keyboard = keyboard_list_groups(group_list, sid)
     cookie.add(sid, dict(action='SETTINGS'))
     bot.send_message(message.chat.id, '<b>Group</b>', reply_markup=keyboard, parse_mode='HTML')
     logger.debug('settings')


@bot.message_handler(commands=['list'])
def view_list_groups(message):
    """ View list groups. Create cookie
      """
    group_list =  db.get_all_group()
    sid = cookie.id
    keyboard = keyboard_list_groups(group_list, sid)
    cookie.add(sid, dict(action='GROUP DETAIL'))
    bot.send_message(message.chat.id, '<b>Groups</b>', reply_markup=keyboard, parse_mode='HTML')


#TODO работает
@bot.message_handler(commands=['last'])
def send_last_posts(message):
    # View for convert cnt from  string format to int format.
    str_range = map(str, range(1,6)) # '1','2'...'5'
    l_str_cnt = list(filter( lambda x: x in message.text, str_range))
    cnt = int(l_str_cnt[0]) if l_str_cnt else 3

    sid = cookie.id
    cookie.add(sid, dict(action='POST EXPAND'))

    last_posts = db.get_last_posts(cnt)
    for post in last_posts:
        keyboard = keyboard_last_posts(post, sid)
        group = post.group.name
        created_at = time.strftime("%H:%M %d-%b-%Y",time.localtime(post.date))
        text = u'<code>{time}</code>\n<b>{group}</b>\n{text}...'.format(time=created_at, group=group, text=post.text[:200])
        bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='HTML', disable_web_page_preview=True)


def edit_message(call, post, keyboard):
    """ Edit, this rewrite text in post. This do expande message.
       """
    id = call.message.chat.id
    mid = call.message.message_id
    created_at = time.strftime("%H:%M %d-%b",time.localtime(post.date))
    group = post.group.name
    ## add url in post
    url = 'http://vk.com/{url}'.format(url=post.group.url)

    ## if post very big. Do limited post 3000.
    if post.photos and len(post.text) < 3000:
        text = u'<b>{group}</b>  <code>{time}</code>\n{photo}\n{text}'.format(time=created_at, url=url, group=group, text=post.text, photo=post.photos)
    else:
        text = u'<b>{group}</b>  <code>{time}</code>\n{text}'.format(time=created_at, group=group, text=post.text[:1000])

    #text = post.text[:100] #TODO For debug
    try:
       bot.edit_message_text(chat_id=id, message_id=mid, text=text, reply_markup=keyboard, parse_mode="HTML")
    except Exception as e:
        logger.error('Post edit:{}'.format(e))


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
    edit_message(call, post, keyboard)


def send_info(call, post_id):
    post  = db.get_post_extand(post_id)
    group = db.get_describe_group(post.group.name)

    logger.debug('{} {} {}'.format(post_id, post,  group))
    if group:
        text = "<strong>{name}</strong>\n <strong>tel: {phone}</strong>\n {info}\n {photo}".format(name=group.name.encode('utf-8'),
                                      info=group.description.encode('utf-8'), photo=group.photo, phone=group.phone)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id=call.message.message_id, text=text, parse_mode='HTML')

    else:
        logger.error('Info at group')


def choose_next_post(call, sid):
    ## user click next or prev post.

    d_session =  cookie.get(sid)
    group_id = int(d_session.get('group'))
    page  = int(d_session.get('page'))
    post = db.get_post_from_group(group_id, page)
    group = db.get_group(group_id)
    keyboard = keyboard_next_page(group, sid)


    if post:
        edit_message(call, post, keyboard)

    else:
         logger.debug('Post no found:')


@bot.callback_query_handler(func=lambda call:True)
def callback_data(call):
    """ callback button
       """
    if call.message:
        dict_callback = json.loads(call.data)
        cookie_uuid = dict_callback.get('id')
        data_for_session = cookie.get(cookie_uuid)
        logger.debug('COOKIE BODY:{}'.format(data_for_session))

        if data_for_session:
            action = data_for_session.get('action')
            callback_button = dict_callback.get('button')
            logger.debug('ACTION:{} '.format(action))

            if action == 'POST EXPAND':
                logger.debug('POST EXPAND')
                cmd = dict_callback.get('cmd')
                post_id = callback_button

                if cmd == 0:
                    send_expanded_post(call, post_id)

                elif cmd ==1:
                    send_info(call, post_id)

            elif action == 'GROUP DETAIL':
                ID_GROUPS_ALL = [i.id for i in db.get_all_group()]
                page = int(data_for_session.get('page', 0))
                group_id = None

                ## previous page
                if callback_button == '\U000023E9':
                    page += 1 if page is not 30 else 0
                    group_id = data_for_session.get('group')

                ## next page
                elif callback_button == '\U000023EA':
                    page -= 1 if page is not 0 else 0
                    group_id = data_for_session.get('group')

                elif callback_button in ID_GROUPS_ALL:
                    page = 0
                    group_id = int(callback_button)

                else:
                    logger.debug('ELSE')

                new_cookie = dict(group = group_id, page=page, action='GROUP DETAIL')
                cookie.add(cookie_uuid, new_cookie)
                choose_next_post(call, cookie_uuid)

            elif action == 'SETTINGS':
                pass

        else:
            logger.debug(call.data)
