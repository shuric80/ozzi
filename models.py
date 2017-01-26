#!../bin/python
#-*- coding:utf-8 -*-
import sys
from datetime import datetime
import enum

from sqlalchemy import Table, Column, \
    Integer,Unicode, \
    DateTime, Enum

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint

import config
if config.DEBUG:
    import sys
    sys.dont_write_bytecode = True

engine = create_engine('sqlite:///telegram_bot.db', echo=False)
Base = declarative_base()


class TypeGroup(enum.Enum):
    Event = 'E'
    Inform = 'I'
    School = 'S'
    
    
class Group(Base):

    __tablename__ = 'group'

    id = Column( Integer, primary_key=True)
    title = Column( Unicode(20), nullable=False)
    description = Column(Unicode(512))
    photo = Column(Unicode(128))
    email = Column(Unicode(62))
    phone = Column(Unicode(12))
    url = Column( Unicode(50), nullable=True)
    #TODO вставить Enum
    #type_group = Column('type',Enum(TypeGroup))
    
    posts = relationship('Post', backref= backref('group', lazy = 'joined'))

    def __repr__(self):
        return '<Group:%s>' % self.name


class Post(Base):

    __tablename__ = 'post'

    id  = Column( Integer, primary_key = True)
    tstamp = Column( DateTime, default = datetime.utcnow)
    date = Column('Created',Integer, nullable = False)
    text = Column( 'Content', Unicode(4096))
    photos = Column( 'Photo', Unicode(512), nullable = True)

    group_id =  Column( Integer, ForeignKey('group.id'))
