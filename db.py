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
    btns = session.query(Group.name).all()
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
    q_post = session.query(Post).join(Post.group). \
             filter(Group.name== name).all()
    post = q_post[num] if len(q_post) > num else None
    session.close()
    return post


def update_db():

    groups = session.query(Group)
    for group in groups.all():
        ext, posts = read_content(group.url)
        group.description = ext['description']
        group.photo = ext['photo']
        group.name = ext['name']
        group.phone = ext['phone']
        group.email = ext['email']
        group.desc = ext['desc']
        for i in posts:
            post = Post(
                text = i['text'],
                #photo = i['photo'],
                group = group,
                date = i['date']
            )
            session.add(post)
            
        session.add(group)

    session.commit()
    session.close()
