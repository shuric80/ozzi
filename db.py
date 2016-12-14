#-*- coding:utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
from models import engine
from models import Post, EventMenu, Tag, Group

from view import logger
import config
from parser import read_content


Session = sessionmaker(bind = engine)
session = Session()


def mainKeyboard():
    #menu = [q[0] for q in session.query(EventMenu.name).all()]
    #return menu[:3]
    btns = session.query(Group.group).all()
    session.close()
    return btns


def groupAll():
    groups = session.query(Group).all()
    session.close()
    return groups

    
def tagAll():

    tags = [q[0] for q in session.query(Tag.tag).all()]
    session.close()
    return tags


def postUseTag(tag, page = 0):
    q_posts = session.query(Post).join(Post.tags). \
                 filter(Tag.tag == tag).all()
    session.close()
    return q_posts[page]


def postInGroup(name, num=0):
    #logger.debug(name)
    q_post = session.query(Post).join(Post.group). \
                 filter(Group.group== name).all()
    post = q_post[num] if len(q_post) > num else None
    session.close()
    return post


def update_db():
    groups = session.query(Group)
    for group in groups.all():
        #posts_tm = session.query(Post.created_at).filter_by(group=group).all()
        posts_wall = read_content(group.url_vk)
        for iter_post in posts_wall:

            post = Post(
                content = iter_post.get('text'),
                photo = iter_post.get('photo'),
                group = group,
                created_at = iter_post.get('date',0)
            )
            session.add(post)

    session.commit()
    session.close()
