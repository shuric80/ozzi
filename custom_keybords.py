#-*- coding:utf-8 -*-

import time
import json
from telebot import types
from log import logger

def keyboard_menu_settings(d_input):
    keyboard = types.InlineKeyboardMarkup(row_width =1)
    button = types.InlineKeyboardButton(text = 'Choose groups', callback_data = json.dumps(dict(id = d_input['id'])))
    keyboard.add(button)
    return keyboard


def keyboard_settings(d_input):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    l_btn = list()

    for btn in d_input['groups']:
        emoji = '\U00002705' if btn.id in d_input['l_like'] else '\U0000274C'
        btn_title =' '.join([ emoji, btn.name])
        callable_button = types.InlineKeyboardButton(
            text = btn_title, callback_data = json.dumps(dict(id = d_input['id'], button = btn.id))
        )
        l_btn.append(callable_button)

    keyboard.add(*l_btn)
    return keyboard


def keyboard_list_groups(q, id):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    l_btns = list()
    for btn in q:
        callable_button = types.InlineKeyboardButton(
            text = btn.name, callback_data= json.dumps(dict(id = id, button=btn.id)))
        l_btns.append(callable_button)

    keyboard.add(*l_btns)
    return keyboard


def keyboard_last_posts(post, id):
    created_at = time.strftime("%H:%M %d-%b-%Y",time.localtime(post.date))
    group = post.group.name
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    callable_button = types.InlineKeyboardButton(text='Expand', callback_data=json.dumps(dict(id =id, button=post.id , cmd=0)))
    #description_button = types.InlineKeyboardButton(text='Info', callback_data=json.dumps(dict(id = cookie_uuid, button = post.id, cmd=1)))
    url_button = types.InlineKeyboardButton(text='Group', url='http://vk.com/{url}'.format( url=post.group.url))
    #text = u'<code>{time}</code>\n<b>{group}</b>\n{text}...'.format(time=created_at, group=group, text=post.text[:200])
    keyboard.add(callable_button)
    return keyboard


def keyboard_next_page(group, sid):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keys = list()
    for i in ['\U000023EA', '\U000023E9']:
        btn = types.InlineKeyboardButton(text = str(i), callback_data = json.dumps(dict(id=sid, button=i.upper())))
        keys.append(btn)

    #group = db.get_group(group_id)
    keys.append(types.InlineKeyboardButton(text='Group', url='http://vk.com/%s'%group.url))
    keyboard.add(*keys)

    return keyboard
