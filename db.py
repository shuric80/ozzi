#-*- coding:utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from models import engine
from models import Post, MainMenu, Tag, Group

from view import logger
import config
import transaction

logger.info('Run DB module.')

Session = sessionmaker(bind = engine)
session = Session()


def readGroup(group, page):
    """
    return post.
    d_input ={ 'group':'***','page':0, 'tag':'***'}

    """
    logger.debug('READ GROUP:%s \t PAGE:%s' % (group, page))
    with transaction.manager:
        result = session.query(Post).join(Post.group).filter(
            Group.label == group.lower()).order_by(~Post.date)


    return result[page] if page < result.count() else None


def readTag(tag, page):
    #tag = session.query(Tag.title).filter_by(id = tag).one()[0]
    #ret = session.query(Post).join(Post.tags).filter(Tag.title == tag).order_by(~Post.date)[page]
    #session.close()
    return None



def addContent(d_input):
    """
    Add post in DB
      """
    posts = list()
    with transaction.manager:

        for row in d_input:
            post  = Post(
                content = row['text'],
                photo = row['photo'],
                date = row['date'],
                group = row['group'])

        #for tag in row['tags']:
        #    post.tags.append(tag)

            session.add(post)

    session.commit()
    session.close()



def groupMenu():
    with transaction.manager:
        q = session.query(Group).all()

    session.close()
    return q


def tagMenu():
    with transaction.manager:
        q = session.query(Tag).all()


    session.close()
    return q


def eventMenu():
    with transaction.manager:
        q = session.query(Event).all()

    sesson.close()
    return q


def mainMenu():
    with transaction.manager:
        q = session.query(MainMenu).all()

    session.close()
    return q
