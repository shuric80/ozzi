# !/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import ast
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
""" Request and parsing posts for wall groups.
    Use public API http://vk.com
   """

CNT  = 10

def request_posts(domain):
    url = 'https://api.vk.com/method/wall.get?domain=' + \
        domain+'&count=%d&v=5.3' % CNT
    response = urllib2.urlopen(url)
    body = response.read()
    return body

def downloadPhoto(photo):
    photo_url = photo.replace('\\/','/')
    photo_name = photo.split('/')[-1]
    urllib.urlretrieve(photo_url, 'static/%s' % photo_name)
    return photo_name


def read_content(group):
    url = group['url']
    ret = request_posts(url)
    dict_posts = ast.literal_eval(ret)['response']['items']
    l_output = list()
    for post in dict_posts:
        text = post.get('text', None)
        attachments = post.get('attachments')
        date = post['date']

        if type(attachments) == list:
            ext_photo = attachments[0].get('photo',None)
            if ext_photo:
                photo = ext_photo.get('photo_130', None)

        else:
            photo = None

        if photo:
            photo_path = downloadPhoto(photo)

        l_output.append( dict(text=text, photo=photo,
                                date=date, group=group['name']))

    return l_output


def updateDB():
    pass





if __name__ == '__main__':
   if len(sys.argv) == 2:
      url = sys.argv[1]
      sys.stdout.write(url)
