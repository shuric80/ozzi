#!../bin/python
#-*- coding:utf-8 -*-
import sys
from datetime import datetime

from sqlalchemy import Table, Column, Integer,Unicode, Date
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

import config


engine = create_engine('sqlite:///telegram_bot.db', echo=False)
Base = declarative_base()

association_table = Table( 'association', Base.metadata,
                           Column( 'tag_id',Integer, ForeignKey('tag.id')),
                           Column( 'post_id', Integer,ForeignKey('post.id'))
)

class Button:
    label = Column( Unicode(50), nullable=False, unique=True)
    handler = Column(Unicode(50), nullable=False, unique=True)


class MainMenu(Button,Base):

    __tablename__ = 'main'
    id = Column( Integer, primary_key=True)


class Group(Button,Base):

    __tablename__ = 'group'
    id = Column( Integer, primary_key=True)
    vk_url = Column( Unicode(100), nullable=True, unique=True)
    posts = relationship('Post', backref="group")


class Tag(Button,Base):

    __tablename__ = 'tag'
    id = Column( Integer, primary_key=True)
    synonyms = Column( Unicode(300))


class Post(Base):

    __tablename__ = 'post'

    id  = Column( Integer, primary_key = True)
    tstamp = Column( Date, default = datetime.utcnow)
    content = Column( 'Content', Unicode(4000))
    photo = Column( 'Photo', Unicode(50), nullable = True)
    group_id =  Column( Integer, ForeignKey('group.id'))
    date = Column(Integer, nullable=False)

    tags = relationship( 'Tag',
                         secondary = association_table,
                         backref = backref('posts'))
