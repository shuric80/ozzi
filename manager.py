#!/env/bin/python
#-*- coding:utf-8 -*-

import os
import sys
import argparse

import config
import db
from parser import read_vk_content
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

def update_posts():
    groups = db.get_all_group()
    r = True
    for g in groups:
        ext, l_ret = read_vk_content(g.url)
        r &= db.update_db(g, l_ret)
        r &= db.update_description_group(g, ext)

    return r



def add_groups():
    r = db.add_groups(config.GROUPS)
    return r


if __name__ == '__main__':
    logger.info('start manager')
    if args.cmd == 'update':

        r = add_groups()
        r &= update_posts()

        if r:
            logger.info('Update done')
        else:
            logger.error('Update is fail.')
