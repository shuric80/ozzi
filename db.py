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

def getTagsObject():
    obj_tags = session.query(Tag).all()
    session.close()
    return obj_tags

def getTags():

    tags =  session.query(Tag.tag).all()
    session.close()
    ret= list()

    for i in tags:
        ret.append( i[0])

    return ret


def getContent( tag, page):

    query_post = session.query(
        Post.photo_path, Post.content).join(Post.tags). \
        filter(Tag.tag == tag). \
        order_by(Post.tstamp). \
        all()

    session.close()

    try:
        ret = query_post[page]

    except IndexError, e:
        logging.error(e)
        ret = None

    return ret

def addContent(d_input):
    """
    Add post in DB
    """
    posts = list()

    for row in d_input:
        post  = Post(
            content = row['text'],
            photo_path = row['photo'],
            date=row['date'],
            group = row['group'])

        for tag in row['tags']:
            post.tags.append(tag)

            session.add(post)

        session.commit()
        session.close()



def  getAllGroups():
    """ return list all groups   {'name':'8888','url':'***'}
      """
    q = session.query(Group).all()
    return q
