#-*- coding:utf-8 -*-
import sys
sys.dont_write_bytecode = True


import sys

from sqlalchemy.orm import sessionmaker

from models import engine
from models import Base
from models import EventMenu, Group, Post, Tag

"""
   create - Create db
    init - initialize data db
  """


def create():
    Base.metadata.create_all(engine)
    print 'Done.'


def init():
    Session = sessionmaker(bind=engine)
    session = Session()

    menu = list()
    menu.append( EventMenu(name = u'Events'))
    menu.append( EventMenu(name = u'Schools'))
    menu.append( EventMenu(name = u'News'))
    for i in menu:
        session.add(i)

    tags = list()
    tags.append(Tag(tag = 'Salsa'))
    tags.append(Tag(tag = u'Salsa on2'))
    tags.append(Tag(tag = u'Social'))
    tags.append(Tag(tag = u'Bachata'))
    tags.append(Tag(tag = u'Lesson'))
    for i in tags:
        session.add(i)
    session.commit()

    post = Post(content = u'вечеринка!!!', photo_path = u'static/1.jpeg')
    post.tags.append(tags[0])
    post.tags.append(tags[2])
    #post.groups.append(group[0])
    session.add(post)

    post = Post(content = u'afasdfadsf',photo_path = u'static/2.jpeg')
    post.tags.append(tags[0])
    session.add(post)

    group = list()
    g = Group(group = u'2mambo',url_vk = u'/2mamboproject')
    g.posts.append(post)
    group.append(Group(group = u'Mambotime', url_vk = u'/mambotime'))
    group.append(Group(group = u'Salsa open', url_vk = u'/salsaopenmsk'))
    group.append(Group(group = u'Salsa-Jam', url_vk = u'/salsa_jam'))
    group.append(Group(group = u'Sierra Maestro',url_vk = u'/sierra_maestra_moscow'))
    group.append(g)
    for i in group:
        session.add(i)

    session.commit()


if  __name__ == '__main__':
    if len(sys.argv) == 1:
        print """ Databases.
                  command line = /'create/' or /'init/'

                 """

    elif sys.argv[1] == 'create':
        create()

    elif sys.argv[1] == 'init':
        init()

    sys.exit(0)
