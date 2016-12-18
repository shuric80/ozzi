#-*- coding:utf-8 -*-
from view import logger
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

    session.close()
    return group



def groupAll():
    with transaction.manager:
        groups = session.query(Group)

    session.close()
    return groups


def tagAll():
    with transaction.manager:
        tags = [q[0] for q in session.query(Tag.tag).all()]

    session.close()
    return tags

def getPost(id):
    with transaction.manager:
        post = session.query(Post).get(id)

    session.close()
    return post

def postUseTag(tag, page = 0):
    with transaction.manager:
        q_posts = session.query(Post).join(Post.tags). \
              filter(Tag.tag == tag).all()

    session.close()
    return q_posts[page]


def postInGroup(group_id, num=0):
    with transaction.manager:
        post = session.query(Post).join(Post.group) \
               .filter(Group.id== group_id) \
               .offset(num) \
               .first() \

    session.close()
    return post


def lastPosts(cnt =5):
    cnt = cnt if 0 < cnt < 10 else 5
    with transaction.manager:
        posts = session.query(Post).order_by(Post.date.desc()).limit(cnt)

    session.close()
    return posts


    
def update_db():
   
    groups = session.query(Group)
    for group in groups.all():
        vk_group, vk_posts = read_content(group.url)

        group.description = vk_group['description']
        group.photo = vk_group['photo']
        group.name = vk_group['name']
        group.phone = vk_group['phone']
        group.email = vk_group['email']
        group.desc = vk_group['desc']
        for post in vk_posts:
            if session.query(Post).join(Group). \
               filter(Post.date == post['date']). \
               filter(Group.name == vk_group['name']).count()==0:
                post_db = Post(
                    text = post['text'],
                    photos = post['photo'][0] if post['photo'] else None,
                    group = group,
                    date = post['date']
                )
                session.add(post_db)

            else:
                logger.debug('Post missed.')


            
        session.add(group)

    session.commit()
    session.close()
