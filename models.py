#!../bin/python
#-*- coding:utf-8 -*-
import sys
from datetime import datetime

from sqlalchemy import Table, Column, Integer,Unicode, Date
from sqlalchemy import ForeignKey, create_engine
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///telegram_bot.db', echo=False)
Base = declarative_base()

association_table = Table('association', Base.metadata,
                          Column('tag_id',Integer, ForeignKey('tag.id')),
                          Column('post_id', Integer,ForeignKey('post.id'))
)

class MainMenu(Base):
    __tablename__ = 'main'
    id = Column(Integer, primary_key=True)
    menu = Column(Unicode(20), nullable=False)

    def __init__(self, menu):
        self.menu = menu

    def __repr__(self):
        return '%r' % self.menu

class Group(Base):
    __tablename__ = 'group'
    id = Column(Integer, primary_key=True)
    group = Column( Unicode(20), nullable=False)
    vk_address = Column( Unicode(50), nullable=True)

    posts = relationship('Post', backref="group")

    def __init__(self, group, vk_address=None):
        self.group = group
        self.vk_address = vk_address

    def __repr__(self):
        return '%r' % self.group
    

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True)
    tag = Column( Unicode(30), nullable=False)

    def __init__(self, tag):
        self.tag = tag

    def __repr__(self):
        return '%s' % self.tag
   

class Post(Base):
    __tablename__ = 'post'
    id  = Column(Integer, primary_key=True)
    time_create = Column(Date, default=datetime.utcnow)
    post = Column('Post', Unicode(255))
    photo = Column('Photo', Unicode(50), nullable = True)
    group_id =  Column(Integer, ForeignKey('group.id'))

    tags = relationship("Tag",
        secondary= association_table,
        backref=backref('posts'))

    def __init__(self, post, photo =None):
        self.post = post
        self.photo = photo

    


