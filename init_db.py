#-*- coding:utf-8 -*-
import sys
sys.dont_write_bytecode = True

import sys
import types
from sqlalchemy.orm import sessionmaker
from models import engine
from models import Base
from models import EventMenu, Group, Post, Tag
from db import update_db
import config

"""
   create - Create db
    init - initialize data db
  """



def create_db():
    Base.metadata.create_all(engine)
    

def init_db():
    Session = sessionmaker(bind=engine)
    session = Session()

    groups = config.GROUPS
    assert(type(groups) == types.TupleType)
    for group in groups:
        db_group = Group()
        db_group.name = group['name']
        db_group.url = group['url']

        session.add(db_group)
    
    session.commit()


def update():
    update_db()

if len(sys.argv)==1:
    create_db()
    init_db()
    update_db()

elif sys.argv[1] == 'create':
    create_db()

elif sys.argv[1] == 'init':
    init_db()

elif sys.argv[1] == 'update':
    update_db()

    
else:
    sys.stderr.write('Error argument')
    sys.exit(-1)

sys.stdout.write('Done')
sys.exit(0)
