#!/env/bin/python
#-*- coding:utf-8 -*-

import os
import sys
import argparse
import shortuuid
from celery import Celery
from celery.schedules import crontab
from datetime import timedelta
import time

import config
import db
from parser import read_vk_content
from log import logger
from server import bot, celery, app


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
celery = Celery('ozzi', broker = config.CELERY_BROKER_URL)

celery.conf.beat_schedule = {
	# executes every night at 4:15
	'every-day': {
		'task': 'user.checkaccounts',
		'schedule': crontab(minute='*/30', hour='7-22')
	}
}


@celery.task(name = 'user.checkaccounts')
def update_posts():
    logger.info('UPDATE POSTS')
    groups = db.get_all_group()
    r = True
    for g in groups:
        ext, l_ret = read_vk_content(g.url)
        r &= db.update_db(g, l_ret)
        r &= db.update_description_group(g, ext)

    return r


def add_groups():
    ##
    logger.info('ADD/RM GROUPS')
    r = db.add_groups(config.GROUPS)
    return r

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Initialize database')
    parser.add_argument('cmd', choices=['update','addgroup','migrate','upgrade','runbot','runserver'])
    args = parser.parse_args()

    logger.info('start manager')
    r = 0

    if args.cmd == 'update':
        ## update posts in database
        r = update_posts()

    elif args.cmd == 'addgroup':
        ## add group to database
        r = add_groups()

    elif args.cmd == 'migrate':
         ## migrate db
         os.system('alembic revision --autogenerate -m "{}"'.format(shortuuid.uuid()))

    elif args.cmd == 'upgrade':
         ## update tables database
         os.system('alembic upgrade head')

    elif args.cmd == 'runbot':
        ## run bot
        bot.polling()

    elif args.cmd == 'runserver':
        bot.remove_webhook()
        time.sleep(0.5)
        bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
                certificate=open(config.WEBHOOK_SSL_CERT, 'r')
                )
        app.run(
            host = config.LOCAL_HOST,
            port = config.LOCAL_PORT,
            debug = config.DEBUG,
            #ssl_context = (config.WEBHOOK_SSL_CERT, config.WEBHOOK_SSL_PRIV)
        )

    else:
        pass

    logger.info('Update is {}'.format(['fail','done'][r]))
