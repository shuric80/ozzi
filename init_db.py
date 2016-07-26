#-*- coding:utf-8 -*-
import sys
sys.dont_write_bytecode = True


import sys

from sqlalchemy.orm import sessionmaker

from models import engine
from models import Base
from models import MainButton, Group, Post, Tag

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
    menu.append( MainButton(label = u'Tags'))
    menu.append( MainButton(label = u'Groups'))
    menu.append( MainButton(label = u'Last'))
    for i in menu:
        session.add(i)

    tags = list()
    tags.append(Tag(title = u'Salsa', synonyms = u'сальса, кубано, кубинская, афро, румба, касино'))
    tags.append(Tag(title = u'Mambo', synonyms = u'линейка, мамбо, salsa on2, NY '))
    tags.append(Tag(title = u'Social', synonyms = u'social, вечеринка, соушел'))
    tags.append(Tag(title = u'Lesson', synonyms = u'урок, мастер класс, семинар'))
    tags.append(Tag(title = u'XXX', synonyms = u'бачата, кизомба, bachata, kizomba'))



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
    g = Group(name = u'2mambo',vk_url = u'2mamboproject')
    #g.posts.append(post)
    group.append(Group(name = u'Mambotime', vk_url = u'mambotime'))
    group.append(Group(name = u'Salsa open', vk_url = u'salsaopenmsk'))
    group.append(Group(name = u'Salsa-Jam', vk_url = u'salsa_jam'))
    group.append(Group(name = u'Sierra Maestro',vk_url = u'sierra_maestra_moscow'))
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
