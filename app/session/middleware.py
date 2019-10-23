from app.user.models import User
from app.session.models import Session
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

        user_id = await Session.get(session_key, redis=app['redis'])
        if not user_id:
            raise web.HTTPForbidden

        request['session'] = session_key
        async with app['db'].acquire() as conn:
            request['user'] = await User.get_by_id(user_id, conn=conn)
        return await handler(request)
    return inner
    
