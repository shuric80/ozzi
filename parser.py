# !/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
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

def read_content(url_address):
    ret = request_posts(url_address)
    dict_posts = ast.literal_eval(ret)['response']['items']

    for post in dict_posts:
        text = post.get('text', None)
        attachments = post.get('attachments')
        photos = list()
        date = post['date']
        if type(attachments) == list:
            for photo in attachments:
                photos.append(photo.get('photo', None))
        else:
            print 'Warning.'

    return dict(text=text, photos=photos, date=date)

if __name__ == '__main__':
   if len(sys.argv) == 2:
      url = sys.argv[1]
      sys.stdout.write(url)
