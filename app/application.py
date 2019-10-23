from aiohttp import web
import aiopg.sa
import logging
import sys

from app.settings import config


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format='%(asctime)s | [%(levelname)s] | %(message)s')


async def init_pg(app):
    conf = app['config']['pg']
    engine = await aiopg.sa.create_engine(
        database=conf['database'],
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        minsize=conf['minsize'],
        maxsize=conf['maxsize'],
    )
    app['db'] = engine

async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


def create_app():
    application = web.Application()
    application['config'] = config
    application.on_startup.append(init_pg)
    application.on_cleanup.append(close_pg)
    return application

application = create_app()

