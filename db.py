#-*- coding:utf-8 -*-
from view import logger
from sqlalchemy.orm import sessionmaker

from init_db import engine
from models import Post, Group

from view import logger
import config
from parser import read_content


Session = sessionmaker(bind = engine)
session = Session()


def get_post_extand(id):
    post = session.query(Post).get(id)
    return post


def get_all_group():
    groups = session.query(Group)
    return groups


def get_last_posts(cnt =5):
    cnt = cnt if 0 < cnt < 10 else 5
    posts = session.query(Post).order_by(Post.date.desc()).limit(cnt)
    return posts


def get_describe_group(name):
    describe = session.query(Group).filter_by(list_names =name).first()
    return describe


def update_db():

    groups = session.query(Group)
    for group in groups.all():
        vk_group, vk_posts = read_content(group.url)
        group.description = vk_group['description']
        group.photo = vk_group['photo']
        group.name = vk_group['name']
        group.phone = vk_group['phone']
        group.email = vk_group['email']
        group.desc = vk_group['desc']
        for post in vk_posts:
            if session.query(Post).join(Group). \
                filter(Post.date == post['date']). \
                filter(Group.name == vk_group['name']).count()==0:
                post_db = Post(
                        text = post['text'],
                        photos = post['photo'][0] if post['photo'] else None,
                        group = group,
                        date = post['date']
                    )
                session.add(post_db)

            else:
                logger.debug('Post missed.')
           
        session.add(group)

    try:
        session.commit()
    except:
        session.rollback()
    finally:       
        session.close()

    return True

    
def get_post_from_group(group_id, num=0):
    post = session.query(Post).join(Post.group). \
             filter(Group.id== group_id)[num]
    #post = q_post[num] if len(q_post) > num else None
    return post

