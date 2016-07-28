#-*- coding:utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from models import engine
from models import Post, MainButton, Tag, Group

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
            ret = session.query(Post).join(Post.group).filter(Group.name == sgroup).order_by(~Post.date)[page]
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


def getTagsButton():
    q = session.query(Tag).all()
    return q

def getGroupsButton():
    q = session.query(Group).all()
    return q

def getMainButton():
    q = session.query(MainButton).all()
    return q
