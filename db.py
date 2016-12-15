#-*- coding:utf-8 -*-
import logging
from sqlalchemy.orm import sessionmaker
import transaction

from models import engine
from models import Post, EventMenu, Tag, Group

from view import logger
import config
from parser import read_content


Session = sessionmaker(bind = engine)
session = Session()


def mainKeyboard():
    with transaction.manager as t:
        btns = session.query(Group.id).all()
        t.note('test')
    
    return btns

def groupID(id):
    with transaction.manager:
        group = session.query(Group).filter_by(id=id).first()
    
    return group


def groupAll():
    with transaction.manager:
        groups = session.query(Group).all()
    
    return groups


def tagAll():
    with transaction.manager:
        tags = [q[0] for q in session.query(Tag.tag).all()]
    
    return tags


def postUseTag(tag, page = 0):
    with transaction.manager:
        q_posts = session.query(Post).join(Post.tags). \
              filter(Tag.tag == tag).all()
    
    return q_posts[page]


def postInGroup(group_id, num=0):
    q_post = session.query(Post).join(Post.group). \
             filter(Group.id== group_id).all()
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
                photos = i['photo'][0] if i['photo'] else None,
                group = group,
                date = i['date']
            )
            session.add(post)
            
        session.add(group)

    session.commit()
    session.close()
