#!../bin/python
#-*- coding:utf-8 -*-
import sys
from datetime import datetime
import enum

from sqlalchemy import Table, Column, \
    Integer,Unicode, \
    DateTime, Enum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy import UniqueConstraint
from base import Base

class Group(Base):

    __tablename__ = 'group'

    id = Column( Integer, primary_key=True)
    name = Column('name', Unicode(20), unique=True, nullable=False)
    description = Column('description', Unicode(512))
    photo = Column('photo_logo', Unicode(128))
    email = Column('email', Unicode(62))
    phone = Column('phone', Unicode(12))
    url = Column( Unicode(50), nullable=True, unique=True)
    posts = relationship('Post', backref= backref('group', lazy = 'joined'))

    def __repr__(self):
        return '<Group:%s>' % self.name


class Post(Base):

    __tablename__ = 'post'

    id  = Column( Integer, primary_key = True)
    tstamp = Column( DateTime, default = datetime.utcnow)
    date = Column('created',Integer, nullable = False)
    text = Column( 'content', Unicode(4096))
    photos = Column( 'photo', Unicode(512), nullable = True)

    group_id =  Column( Integer, ForeignKey('group.id'))
