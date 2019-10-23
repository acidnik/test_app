from aiohttp import web

from app.user.handlers import login as user_login, logout as user_logout


def add_routes(router):
    router.add_routes([
        web.get('/api/v1/user/login', user_login),
        web.get('/api/v1/user/logout', user_logout),
    ])
