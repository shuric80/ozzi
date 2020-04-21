#-*- coding:utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

from configobj import ConfigObj

Base = declarative_base()

config = ConfigObj('alembic.ini')
engine = create_engine(config['alembic']['sqlalchemy.url'], echo=False)
