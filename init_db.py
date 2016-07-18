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
init - initialize db
  """

def create():
    Base.metadata.create_all(engine)


def init():
    Session = sessionmaker(bind=engine)
    session = Session()

    menu = list()
    menu.append( MainMenu(u'Events'))
    menu.append( MainMenu(u'Schools'))
    menu.append( MainMenu(u'News'))
    for i in menu:
        session.add(i)

    tag = list()
    tag.append(Tag(u'Salsa'))
    tag.append(Tag(u'Salsa on2'))
    tag.append(Tag(u'Social'))
    tag.append(Tag(u'Bachata'))
    tag.append(Tag(u'Lesson'))
    for i in tag:
        session.add(i)

    post = Post(u'вечеринка!!!',u'static/1.jpg')
    post.tags.append(tag[1])
    post.tags.append(tag[2])
    #post.groups.append(group[0])
    session.add(post)

    group = list()
    g = Group(u'2mambo', u'/2mamboproject')
    g.posts.append(post)
    group.append(Group(u'Mambotime', u'/mambotime'))
    group.append(Group(u'Salsa open', u'/salsaopenmsk'))
    group.append(Group(u'Salsa-Jam', u'/salsa_jam'))
    group.append(Group(u'Sierra Maestro',u'/sierra_maestra_moscow'))
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
