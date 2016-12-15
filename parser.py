# !/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import ast
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
""" Request and parsing posts for wall groups.
    Use public API http://vk.com
   """

import json

CNT  = 10

URL = 'https://api.vk.com/method/wall.get'

def request_posts(domain):

    params = dict(domain=domain, v=5.3, count=CNT, filter='owner')
    res = requests.get(URL, params=params)
    return res.text


def read_content(url_address):
    l_ret = list()
    ret = request_posts(url_address)
    j_posts = json.loads(ret)
    for post in j_posts['response']['items']:
        text = post['text']
        date = post['date']
        attachments = post.get('attachments')
        photo = None

        if not attachments:
            pass

        elif attachments[0]['type'] == 'photo':
            photo = attachments[0]['photo'].get('photo_604')

        elif attachments[0]['type'] == 'video':
            photo = attachments[0]['video'].get('photo_604')

        else:
            photo = None

        repost = post.get('copy_history')

        if repost:
            text = repost[0]['text']
            try:
                photo = repost[0]['attachments'][0]['photo']['photo_604']

            except KeyError:
                photo = None

        l_ret.append(dict(text=text, photo= photo, date=date))

    return l_ret


if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]
        sys.stdout.write(url)
