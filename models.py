#!../bin/python
#-*- coding:utf-8 -*-
import sys
from datetime import datetime

from sqlalchemy import Table, Column, Integer,Unicode, Date
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import config
if config.DEBUG:
    import sys
    sys.dont_write_bytecode = True

engine = create_engine('sqlite:///telegram_bot.db', echo=False)
Base = declarative_base()

association_table = Table( 'association', Base.metadata,
                          Column( 'tag_id',Integer, ForeignKey('tag.id')),
                          Column( 'post_id', Integer,ForeignKey('post.id'))
)

class EventMenu(Base):

    __tablename__ = 'main'

    id = Column( Integer, primary_key=True)
    name = Column( Unicode(20), nullable=False)


class Group(Base):

    __tablename__ = 'group'

    id = Column( Integer, primary_key=True)
    group = Column( Unicode(20), nullable=False)
    url_vk = Column( Unicode(50), nullable=True)

    posts = relationship('Post', backref="group")


class Tag(Base):
    
    __tablename__ = 'tag'

    id = Column( Integer, primary_key=True)
    tag = Column( Unicode(30), nullable=False)

    
class Post(Base):

    __tablename__ = 'post'

    id  = Column( Integer, primary_key = True)
    tstamp = Column( Date, default = datetime.utcnow)
    content = Column( 'Content', Unicode(255))
    photo_path = Column( 'Photo', Unicode(50), nullable = True)
    group_id =  Column( Integer, ForeignKey('group.id'))

    tags = relationship( 'Tag',
        secondary = association_table,
        backref = backref('posts'))
