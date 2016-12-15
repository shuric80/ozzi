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

CNT  = 5

URL = 'https://api.vk.com/method/wall.get'

def request_posts(domain, ext=False):
    params = dict(domain=domain, v=5.3, count=CNT, filter='owner', extended =1, fields= 'description,contacts')
    res = requests.get(URL, params=params)
    return res.text

def serializePost(post):
    text = post['text']
    date = post['date']
    
    photo = list()
    video = list()
    attachments = post.get('attachments')
    if attachments:
    
        for attach in attachments:
            if attach['type'] == 'photo':
                photo.append(attach['photo'].get('photo_604'))

            elif attach['type'] == 'video':
                photo.append(attach['video'].get('photo_604'))
                title = attach['video']['title']
                description = attach['video']['description']

            else:
                pass

    return dict(text=text, date=date, photo = photo)

    
def read_content(url_address):
    l_ret = list()
    ret = request_posts(url_address)
    j_posts = json.loads(ret)
    groups = j_posts['response'].get('groups')
  
    if groups:
        ext = dict(
                    name = groups[0]['name'],
                    description = groups[0]['description'],
                    photo = groups[0]['photo_100'],
                    phone = groups[0]['contacts'][0].get('phone'),
            email = groups[0]['contacts'][0].get('email'),
            desc = groups[0]['contacts'][0].get('desc'),
                              )
        
    for post in j_posts['response']['items']:
        if post['post_type'] == 'post':
            d_post = serializePost(post)
            l_ret.append(d_post)

        elif post['post_type'] == 'copy':
            d_post =serializePost( post['copy_history'][0])
            l_ret.append(d_post)

    return ext, l_ret


if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]
        sys.stdout.write(url)
