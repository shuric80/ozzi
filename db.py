#-*- coding:utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from models import engine
from models import Post, EventMenu, Tag, Group

from view import logger
import config


Session = sessionmaker(bind = engine)
session = Session()


def getMainEvents():

    menu = [q[0] for q in session.query(EventMenu.name).all()]
    logging.debug(menu)
    return menu


def getTags():

    tags = [q[0] for q in session.query(Tag.tag).all()]
    logging.debug(tags)
    return tags


def getTagPost(tag, page = 0):

    query_post = session.query(Post).join(Post.tags). \
                 filter(Tag.tag == tag).order_by(Post.tstamp).all()

    print query_post    
    #return query_post.content #, query_post.photo_path
    
