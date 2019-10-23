from aiohttp import web

from app.db import users
from app.user.models import User
from app.session.models import Session
from app.session.middleware import login_required

import logging

class UserHandlers:
    def __init__(self):
        pass

    async def login(request):
        app = request.app
        login = request.query.get('login')
        password = request.query.get('password')
        logging.info(f"{login} {password} {request.query}")
        if not login or not password:
            raise web.HTTPForbidden
        async with app['db'].acquire() as conn:
            session = await User.auth(login, password, conn=conn)
        if session:
            return web.json_response({'session': session})
        raise web.HTTPForbidden

    @login_required
    async def get(request):
        """
            Получить пользователя по id
            Любой пользователь может получить инфу по любому пользователю
        """
        app = request.app
        user_id = int(request.match_info['user_id'])
        async with app['db'].acquire() as conn:
            user = await User.get_by_id(user_id, conn=conn)
            if user:
                return web.json_response({'user': user.to_dict()})
            raise web.HTTPNotFound

    @login_required
    async def logout(request):
        app = request.app
        user = request['user']
        async with app['db'].acquire() as conn:
            await Session.delete(user.session_key, conn=conn)
        return web.json_response({})


