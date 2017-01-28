#!../bin/python
#-*- coding:utf-8 -*-
import sys
from datetime import datetime
import enum
from configobj import ConfigObj

from sqlalchemy import Table, Column, \
    Integer,Unicode, \
    DateTime, Enum

from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import UniqueConstraint


Base = declarative_base()
# rEad url database
config = ConfigObj('alembic.ini')
engine = create_engine(config['alembic']['sqlalchemy.url'])

TypeGroup = ['SCHOOL', 'EVENT']

class Group(Base):

    __tablename__ = 'group'

    id = Column( Integer, primary_key=True)
    title = Column( Unicode(20), unique=True, nullable=False)
    name = Column(Unicode(30))
    description = Column(Unicode(512))
    photo = Column(Unicode(128))
    email = Column(Unicode(62))
    phone = Column(Unicode(12))
    url = Column( Unicode(50), nullable=True, unique=True)
    types = Column('type',Enum(*TypeGroup))
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
