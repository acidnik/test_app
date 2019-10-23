from aiohttp import web

from app.user.handlers import UserHandlers


def add_routes(router):
    user = UserHandlers
    router.add_routes([
        web.get('/api/v1/user/login', user.login),
        web.get('/api/v1/user/logout', user.logout),
        web.get('/api/v1/user/{user_id:\d+}', user.get),
    ])
