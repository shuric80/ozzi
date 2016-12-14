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
    params = dict(domain=domain, v=5.3, count=CNT)
    res = requests.get(URL, params=params)
    return res.text


def read_content(url_address):
    l_ret = list()
    ret = request_posts(url_address)
    try:
        posts = json.loads(ret)['response']['items']

    except KeyError:
        print url_address
        raise ValueError('test')

    for post in posts:
        text = post.get('text', None)
        attachments = post.get('attachments')
        date = post['date']
        if not attachments:
           l_ret.append(dict(text=text, date=date))
           continue
        
        if attachments[0]['type'] == 'photo':
            try:
                photo = attachments[0]['photo']['photo_1280']
            except KeyError:
                photo = attachments[0]['photo']['photo_130']

        elif attachments[0]['type'] == 'video':
            try:
                photo = attachments[0]['video']['photo_1280']
            except KeyError:
                photo = attachments[0]['video']['photo_130']

        else:
            photo = None
        
        l_ret.append(dict(text=text, photo= photo, date=date))

    return l_ret


if __name__ == '__main__':
   if len(sys.argv) == 2:
      url = sys.argv[1]
      sys.stdout.write(url)
