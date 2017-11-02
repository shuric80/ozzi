#-*- coding:utf-8 -*-
#from view import logger
from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy import create_engine
from models import Post, Group

from log import logger
import config
from parser import read_content
from configobj import ConfigObj

from base import engine, config

session_factory = sessionmaker(bind = engine)
session = scoped_session(session_factory)


def get_post_extand(id):
    q = session.query(Post).get(id)
    return q

def get_all_group():
    q = session.query(Group)
    return q

def get_last_posts(cnt = 5):
    cnt = cnt if 0 < cnt < 10 else 5
    q = session.query(Post).order_by(Post.date.desc()).limit(cnt)
    return q

def get_group(id):
    q = session.query(Group).get(id)
    return q

def get_describe_group(name):
    q = session.query(Group).filter_by(title =name).first()
    return q

def add_group(l_input):
    groups = get_all_group()
    for url in l_input:
        if url not in list(map(lambda x:x.url, groups)):
            group = Group()
            group.url = url

            session.add(group)

    try:
        session.commit()
    except:
        session.rollback()
    finally:
        logger.error('Database uncommited')
        session.close()



def update_db(d_input):
    ## update data in database
     for url, content in d_input.items():
        for post in content['posts']:
            if session.query(Post).join(Group).filter(Post.date == post['date']) \
                .filter(Group.url == url).count()==0:

                post_db = Post(
                        text = post['text'],
                        photos = post['photo'][0] if post['photo'] else None,
                        group = group,
                        date = post['date']
                    )

                session.add(post_db)
            else:
                logger.debug('Post missed.')

    try:
        session.commit()
    except:
        session.rollback()
        logger.error('Database uncommit')
    finally:
        session.close()


def get_post_from_group(group_id, num = 0):
    post = session.query(Post).join(Post.group). \
             filter(Group.id== group_id)[num]
    return post
