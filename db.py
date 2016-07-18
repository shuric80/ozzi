#-*- coding:utf-8 -*-

from sqlalchemy.orm import sessionmaker
from models import engine
from models import Post, EventMenu, Tag, Group

from views import logger

Session = sessionmaker(bind = engine)
session = Session()


def get_main():
    menu = [q[0] for q in session.query(MainMenu.name).all()]
    logging.debug(menu)
    return menu

def get_tags():
    tags = [q[0] for q in session.query(Tag.tag).all()]
    logging.debug(tags)
    return tags

def get_post_tag(tag, pagination = 0):
    query_post = session.query(Post.content, Post.photo_path). \
                 join(Tag.tag == tag).order_by(Post.tstamp).all()[pagination]
    logging.debug(query_post)
    
