#-*- coding:utf-8 -*-
import os
import sys
import types

from sqlalchemy.orm import sessionmaker
from models import engine
from models import Group, Post
#from db import update_db
import config

"""
Use alembic for generate database.
> alembic init migrate
add text in env.py
----
import os
import sys

MODEL_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)),"..")
sys.path.append(MODEL_PATH)

import models
target_metadata = models.Base.metadata
---
> alembic revision --autogenerate -m  'initial'
> alembic upgrade head
"""


def _save_from_config_in_base():
    Session = sessionmaker(bind = engine)
    session = Session()
    
    groups = config.GROUPS
    assert(type(groups) == types.TupleType)
    for group in groups:
        db_group = Group()
        db_group.title = group['title']
        db_group.url = group['url']
        db_group.type = group['type']

        session.add(db_group)
        
    try:
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()



cmd = sys.argv[1] if len(sys.argv) >1 else None

if cmd == 'initialize':
    _save_from_config_in_base()


sys.stdout.write('Done')
sys.exit(0)

