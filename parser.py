# !/usr/bin/python
# -*- coding: utf-8 -*-

import urllib2
import urllib
import ast
import re
import sys

from rutermextract import TermExtractor

import db

import logging
from view import logger

logger.debug("Run parser module")

#reload(sys)
#sys.setdefaultencoding('utf-8')

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
    """
    Download and save photo.
       """
    photo_url = photo.replace('\\/','/')
    photo_name = photo.split('/')[-1]
    urllib.urlretrieve(photo_url, 'static/%s' % photo_name)
    return photo_name


def setTags(text):
    """
    find word and select tag.
       """

    term_exctractor = TermExtractor()
    words_key = list()

    for term in term_exctractor(text):
        words_key.append(term.normalized.encode('utf8'))

    l_output = list()
    db_tags = db.getTagsObject()

    for l_tags  in  db_tags:

        synonyms_tag = [ i.strip() for i in l_tags.synonyms.split(',')]

        for tag in synonyms_tag:
            if tag in words_key:
                l_output.append(l_tags)


    return l_output


def getPostsFromWallGroup(group):
    """
    Get posts
    """
    url = group.vk_url
    ret = request_posts(url)
    dict_posts = ast.literal_eval(ret)['response']['items']
    l_output = list()
    for post in dict_posts:
        text = post.get('text', None).decode('utf8')

        attachments = post.get('attachments')
        date = post['date']

        if type(attachments) == list:
            ext_photo = attachments[0].get('photo',None)
            if ext_photo:
                photo_url = ext_photo.get('photo_604', None).decode('utf8')

        else:
            photo_url = None

        if photo_url:
            photo = downloadPhoto(photo_url)

        #tags = setTags(text)
        tags = []

        l_output.append( dict(text=text,tags=tags, photo=photo,
                              date=date, group=group))

    return l_output




def updateDB():
    groups = db.groupMenu()

    for i in groups:
        data = getPostsFromWallGroup(i)
        db.addContent(data)



if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]
        sys.stdout.write(url)
