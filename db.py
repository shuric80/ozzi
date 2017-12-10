#-*- coding:utf-8 -*-
#from view import logger
from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy import exc
from sqlalchemy import create_engine
from models import Post, Group

from log import logger
from parser import read_content
#from configobj import ConfigObj

from base import engine, config
from config import GROUPS

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

def update_db(name_group, d_input):
    ## update data in database
    group = session.query(Group).filter_by(public_name=name_group).one()

    for post in d_input['posts']:
        if session.query(Post).join(Group).filter(Post.date == post['date']).filter(Group.public_name == name_group).count() == 0:
            post_db = Post()
            post_db.text = post['text']
            post_db.photos = post['photo'][0] if post['photo'] else None
            post_db.group = group
            post_db.date = post['date']

            session.add(post_db)

        else:
            logger.debug('Post missed.')

    status = True
    try:
         session.commit()
    except exc.SQLAlchemyError as e:
         logger.error(e)
         session.rollback()
         status = False
    finally:
         session.close()

    return status


def get_post_from_group(group_id, num = 0):
    post = session.query(Post).join(Post.group). \
             filter(Group.id== group_id)[num]
    return post


def update_groups(l_input):

    #TODO add for rm group
    db_groups = get_all_group()
    ## add group
    for group in l_input:
        if group['name'] not in [g['name'] for g in db_groups]:
            db_group = Group()
            db_group.public_name = group['name']
            db_group.url = group['url']
            session.add(db_group)

    try:
       session.commit()
       logger.info('Commited.')
    except exc.SQLAlchemyError as e:
       session.rollback()
       logger.error('Database rollback.{}'.format(e))
    finally:
       session.close()
       logger.info('Database close')

    return True
