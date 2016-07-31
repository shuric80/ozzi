#-*- coding:utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from models import engine
from models import Post, MainMenu, Tag, Group

from view import logger
import config


Session = sessionmaker(bind = engine)
session = Session()


def getContent( d_input):
    """
    return post.
    d_input ={ 'group':'***','page':0, 'tag':'***'}
     """
    page = d_input['cnt_page']
    id_tag = d_input.get('id_tag', None)
    sgroup = d_input.get('group', None)

    if sgroup:
        try:
            ret = session.query(Post).join(Post.group).filter(
                Group.name ==sgroup).order_by(~Post.date)[page]

        except IndexError:
            ret = None

    elif id_tag:
        tag = session.query(Tag.title).filter_by(id = id_tag).one()[0]
        try:
            ret = session.query(Post).join(Post.tags).filter(Tag.title == tag).order_by(~Post.date)[page]

        except IndexError:
            ret = None

    else:
        ret = None

    session.close()
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

        #for tag in row['tags']:
        #    post.tags.append(tag)

        session.add(post)

    session.commit()
    session.close()



def groupMenu():
    q = session.query(Group).all()
    session.close()
    return q


def tagMenu():
    q = session.query(Tag).all()
    session.close()
    return q


def eventMenu():
    q = session.query(Event).all()
    session.close()
    return q


def mainMenu():
    q = session.query(MainMenu).all()
    session.close()
    return q
