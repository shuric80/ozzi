#-*- coding:utf-8 -*-
from view import logger
from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy import create_engine
from models import Post, Group

from view import logger
import config
from parser import read_content
from configobj import ConfigObj


config = ConfigObj('alembic.ini')
engine = create_engine(config['alembic']['sqlalchemy.url'])

session_factory = sessionmaker(bind = engine)
session = scoped_session(session_factory)


def get_post_extand(id):
    q = session.query(Post).get(id)
    return q


def get_all_group():
    q = session.query(Group)
    return q


def get_last_posts(cnt =5):
    cnt = cnt if 0 < cnt < 10 else 5
    q = session.query(Post).order_by(Post.date.desc()).limit(cnt)
    return q

def get_group(id):
    q = session.query(Group).get(id)
    return q

def get_describe_group(name):
    q = session.query(Group).filter_by(title =name).first()
    return q


def update_db():

    groups = session.query(Group)
    for group in groups:
        vk_group, vk_posts = read_content(group.url)
        group.description = vk_group['description']
        group.photo = vk_group['photo']
        group.name = vk_group['name']
        group.phone = vk_group['phone']
        group.email = vk_group['email']
        group.desc = vk_group['desc']
        for post in vk_posts:
            if session.query(Post).join(Group).filter(Post.date == post['date']).filter(Group.name == vk_group['name']).count()==0:
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

    
def get_post_from_group(group_id, num = 0):
    post = session.query(Post).join(Post.group). \
             filter(Group.id== group_id)[num]
    return post

