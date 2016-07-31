#-*- coding:utf-8 -*-
import sys
sys.dont_write_bytecode = True


import sys

from sqlalchemy.orm import sessionmaker

from models import engine
from models import Base
from models import MainMenu, Group, Post, Tag

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
    menu.append( MainMenu(label = u'Tags', handler = u'TAG'))
    menu.append( MainMenu(label = u'Groups', handler = u'GROUP'))
    menu.append( MainMenu(label = u'Event', handler = u'EVENT'))

    for i in menu:
        session.add(i)

    tags = list()
    tags.append(Tag(label = u'Salsa', handler =u'SALSA'))
    tags.append(Tag(label = u'Mambo', handler = u'MAMBO'))
    tags.append(Tag(label = u'Social', handler = u'SOCIAL'))
    tags.append(Tag(label = u'Lesson', handler = u'LESSON'))
    tags.append(Tag(label = u'XXX', handler = u'XXX'))



    for i in tags:
        session.add(i)

    session.commit()

    #post = Post(content = u'вечеринка!!!', photo_path = u'static/1.jpeg')
    #post.tags.append(tags[0])
    #post.tags.append(tags[2])
    #post.groups.append(group[0])
    #session.add(post)

    #post = Post(content = u'afasdfadsf',photo_path = u'static/2.jpeg')
    #post.tags.append(tags[0])
    #session.add(post)

    group = list()
    group.append(Group(label = u'2mambo', handler = u'2MAMBO',vk_url = u'2mamboproject'))
    group.append(Group(label = u'Mambotime', handler=u'MAMBOTIME', vk_url = u'mambotime'))
    group.append(Group(label = u'Salsa open', handler=u'SALSAOPEN', vk_url = u'salsaopenmsk'))
    group.append(Group(label = u'Salsa-Jam', handler=u'SALSAJEM',vk_url = u'salsa_jam'))
    group.append(Group(label = u'Sierra Maestro', handler=u'SIERRAMAESTRO',vk_url = u'sierra_maestra_moscow'))

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
