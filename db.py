#-*- coding:utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from models import engine
from models import Post, MainButton, Tag, Group

from view import logger
import config


Session = sessionmaker(bind = engine)
session = Session()


def getMainButton():
    """ get all event. Main menu

       """
    q = session.query(MainButton).all()
    session.close()

    return q


def getTagsObject():
    obj_tags = session.query(Tag).all()
    session.close()

    return obj_tags


def getTagsIdTag():

    q =  session.query(Tag.id, Tag.tag).all()
    session.close()
    l_output = list()

    for i in q:
        l_output.append(dict(id = i[0], tag = i[1].encode('utf8')))

    return l_output


def getContent( d_input):
    page = d_input['cnt_page']
    tag = d_input.get('tag', None)
    group = d_input.get('group', None)

    if tag:
        obj = session.query(
            Post.content, Post.photo_path).join(Post.tags). \
            filter(Tag.title == tag).order_by(Post.date).get(page)

    elif group:
        obj = session.query(
            Post.content, Post.photo_path).join(
                Post.group).filter(Group.name == group).order_by(Post.date).get(page)

    session.close()

    return obj

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
