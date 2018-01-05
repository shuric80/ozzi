#-*- coding:utf-8 -*-
#from view import logger
from sqlalchemy.orm import sessionmaker, scoped_session

from sqlalchemy import exc
from sqlalchemy import create_engine
from models import Post, Group, User

from log import logger
#from configobj import ConfigObj

from base import engine, config
from config import GROUPS

session_factory = sessionmaker(bind = engine)
session = scoped_session(session_factory)


def get_user(id):
    return session.query(User).get(id)


def get_group_user(id):
    return session.query(Group).join(Group.users).filter(User.id == id)


def update_users_group(user, l_groups):
    ## update user's prefer groups
    user_db = session.query(User).get(user.id)
    if not user_db:
        user_db = User()
        user_db.id = user.id

    user_db.first_name = user.first_name
    user_db.last_name = user.last_name
    user_db.username = user.username

    user_db.groups = [get_group(id) for id in l_groups]

    session.add(user_db)

    try:
        session.commit()
    except exc.SQLAlchemyError as e:
          logger.error(e)
          session.rollback()
    finally:
        pass


def get_post_extand(id):
    ## return post with full text
    q = session.query(Post).get(id)
    return q


def get_all_group():
    ## list groups
    q = session.query(Group)
    return q


def get_last_posts(user_id, cnt = 5):
    ## return last post for time
    cnt = cnt if 0 < cnt < 10 else 5
    user = get_user(user_id)
    user_groups = [ g.id for g in user.groups]
    q = session.query(Post).join(Group).filter(Group.id.in_(user_groups)) \
                                               .order_by(Post.date.desc()).limit(cnt)
    return q


def get_group(id):
    # group
    q = session.query(Group).get(id)
    return q


def add_group(l_input):
    groups = get_all_group()
    for url in l_input:
        if url not in list(map(lambda x:x.url, groups)):
            group = Group()
            group.url = url


def update_db(group, d_input):
    ## add content to database
    ## input -> name and dict text(str), photo(list), date(int)

    for post in d_input:
        if session.query(Post).join(Group).filter(Post.date == post['date']).filter(Group.id == group.id).count() == 0:
            post_db = Post()
            post_db.text = post['text']
            post_db.photos = post['photo'][0] if post['photo'] else None
            post_db.group = group
            post_db.date = post['date']

            session.add(post_db)

        else:
            logger.debug('Post missed.')

    status = True
    try:
        session.commit()
    except exc.SQLAlchemyError as e:
          logger.error(e)
          session.rollback()
          status = False
    finally:
        #session.close()
        pass

    return status


def get_post_from_group(group_id, num = 0):
    ## for group.id return post with offset num
    post = session.query(Post).join(Post.group).filter(Group.id== group_id)[num]
    return post


def add_groups(l_input):
    #TODO add for rm group
    db_groups = get_all_group()
    l_name_groups = [g.url for g in db_groups]
    ## add group
    for group in l_input:
        if group['url'] not in l_name_groups:
            db_group = Group()
            db_group.name = group['name'] if group['name'] else None
            db_group.url = group['url']
            session.add(db_group)

    status = True
    try:
       session.commit()
       logger.info('Commited.')
    except exc.SQLAlchemyError as e:
       session.rollback()
       logger.error('Database rollback.{}'.format(e))
       status = False
    finally:
       session.close()
       logger.info('Database close')

    return status


def update_description_group(group, d_input):

    group.email = d_input.get('email')
    group.name = d_input.get('name')
    group.description = d_input.get('description')
    #group.desc = d_input.get('desc')
    group.phone = d_input.get('phone')
    group.photo = d_input.get('photo')

    session.add(group)

    status = True
    try:
         session.commit()
    except exc.SQLAlchemyError as e:
         logger.error(e)
         session.rollback()
         status = False
    finally:
        #session.close()
        pass

    return status
