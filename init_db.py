#-*- coding:utf-8 -*-
import os
import sys
import types

from sqlalchemy.orm import sessionmaker
from models import engine
from models import Group, Post
import config
from db import session
from db import update_db

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


def _migrate_database(name_revision):
    arg_rev = ' -m {}'.format(name_revision) if name_revision else None 
    os.system('alembic revision --autogenerate {}'.format(arg_rev))
    os.system('alembic upgrade head')

cmd = sys.argv[1] if len(sys.argv) >1 else None

if cmd == 'initialize':
    _save_from_config_in_base()

elif cmd == 'update':
    update_db()

elif cmd == 'migrate':
    rev = sys.argv[2] if len(sys.argv) >2 else None
    _migrate_database(rev)

else:
    sys.stderr.write('Error command\n')

sys.stdout.write('Done')
sys.exit(0)

