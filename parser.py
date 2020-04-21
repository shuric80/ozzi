import ast
import json
import re
import sys

import requests

import config

URL = 'https://api.vk.com/method/wall.get'
TOKEN = config.VK_TOKEN
CNT = config.CNT


def request_posts(domain, ext=False):
    ## do request to vk.com
    params = dict(domain=domain,
                  v=5.68,
                  count=CNT,
                  filter='owner',
                  extended=1,
                  fields='description,contacts',
                  access_token=TOKEN)
    res = requests.get(URL, params=params)
    return res.text


def serialize_vk_post(post):
    ## serialize post from vk
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
                photo.append(attach['video'].get('photo_640'))
                title = attach['video']['title']
                description = attach['video']['description']
                text = u'Video:{ext}{title}\n{description}'.format(
                    ext=text, title=title, description=description)

            else:
                pass

    return dict(text=text, date=date, photo=photo)


def read_vk_content(url_address):
    l_ret = list()
    ret = request_posts(url_address)
    j_posts = json.loads(ret)
    groups = j_posts['response'].get('groups')

    phone = groups[0]['contacts'][0].get(
        'phone') if groups[0]['contacts'] else None
    email = groups[0]['contacts'][0].get(
        'email') if groups[0]['contacts'] else None
    desc = groups[0]['contacts'][0].get(
        'desc') if groups[0]['contacts'] else None

    if groups:
        ext = dict(name=groups[0]['name'],
                   description=groups[0]['description'],
                   photo=groups[0]['photo_100'],
                   phone=phone,
                   email=email,
                   desc=desc)

    for post in j_posts['response']['items']:
        if post['post_type'] == 'post':
            d_post = serialize_vk_post(post)

            ## if repost
            if 'copy_history' in post:
                d_repost = serialize_vk_post(post['copy_history'][0])
                ## text from repost add text from post
                d_repost['text'] = ('\n...').join(
                    [d_post['text'], d_repost['text']])
                l_ret.append(d_repost)
            else:
                l_ret.append(d_post)

    return ext, l_ret


if __name__ == '__main__':
    if len(sys.argv) == 2:
        url = sys.argv[1]
        sys.stdout.write(url)
