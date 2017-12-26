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



association_table_post_tag = Table('association_post_tag', Base.metadata,
                          Column('post_id', Integer, ForeignKey('post.id')),
                          Column('tag_id', Integer, ForeignKey('tag.id')))


association_table_tag_user = Table('association_tag_user', Base.metadata,
                          Column('user_id', Integer, ForeignKey('user.id')),
                          Column('tag_id', Integer, ForeignKey('tag.id')))

association_table_group_user = Table('association_group_user', Base.metadata,
                          Column('user_id', Integer, ForeignKey('user.id')),
                          Column('group_id', Integer, ForeignKey('group.id')))


class Group(Base):

    __tablename__ = 'group'

    id = Column( Integer, primary_key=True)
    name = Column('name', Unicode(20))
    description = Column('description', Unicode(512))
    photo = Column('photo_logo', Unicode(128))
    email = Column('email', Unicode(62))
    phone = Column('phone', Unicode(12))
    url = Column( Unicode(50), nullable=True, unique=True)

    posts = relationship('Post', backref= backref('group', lazy = 'joined'))
    users = relationship('User', secondary=association_table_group_user, back_populates='groups')

    def __repr__(self):
        return '<Group:{}>'.format(self.name)


class Tag(Base):

    __tablename__ = 'tag'

    id = Column(Integer, primary_key=True)
    name = Column('Tag', Unicode(128), unique=True)

    posts = relationship('Post', secondary=association_table_post_tag, back_populates ='tags')

    def __repr__(self):
        return '<Tag:{}>'.format(self.name)


class Post(Base):

    __tablename__ = 'post'

    id  = Column( Integer, primary_key = True)
    tstamp = Column( DateTime, default = datetime.utcnow)
    date = Column('created', Integer, nullable = False)
    text = Column('content', Unicode(4096))
    photos = Column('photo', Unicode(512), nullable = True)

    group_id =  Column(Integer, ForeignKey('group.id'))
    tags = relationship('Tag', secondary = association_table_post_tag, back_populates='posts')


class DateTime(Base):
    __tablename__ = 'datetime'
    id = Column(Integer, primary_key=True)
    tstamp = Column(DateTime)


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    #message_chat_id = Column(Integer, primary_key = True)

    first_name = Column('first name', Unicode(128))
    last_name = Column('last name',  Unicode(128))
    username = Column('username', Unicode(128))

    real_name = Column('Name', Unicode(128))

    #dates = Column(Integer, ForeignKey('datetime.id'))
    groups = relationship('Group', secondary = association_table_group_user, back_populates='users')
