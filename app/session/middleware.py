from app.user.models import User
from aiohttp import web

def login_required(handler):
    """
        враппер для ручек, требующих авторизации
    """
    async def inner(request):
        app = request.app
        session_key = request.headers.get('authorization')
        if not session_key:
            raise web.HTTPForbidden

        async with app['db'].acquire() as conn:
            user = await User.get_by_session_key(session_key, conn=conn)
        if not user:
            raise web.HTTPForbidden

        request['user'] = user
        return await handler(request)
    return inner
    
