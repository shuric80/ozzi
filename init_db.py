#-*- coding:utf-8 -*-
import os
import sys
import types
import argparse
from sqlalchemy.orm import sessionmaker
from sqlalchemy import exc
from base import engine

from models import Group, Post
import config
from db import session, update_db
from log import logger

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

parser = argparse.ArgumentParser(description='Initialize database')
parser.add_argument('cmd', choices=['update'])
args = parser.parse_args()




d_cmd = dict(update = update_groups)

if args.cmd in d_cmd:
    event = d_cmd.get(args.cmd)()
else:
    logger.error('Error cmd')
    sys.exit(-1)

logger.info('done')
sys.exit(0)
