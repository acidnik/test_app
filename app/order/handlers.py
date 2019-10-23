from aiohttp import web

from app.order.models import Order
from app.session.middleware import login_required

import logging

class OrderHandlers:
    @login_required
    async def orders(request):
        """
            история заказов для авторизованного пользователя
        """
        app = request.app
        user = request['user']
        async with app['db'].acquire() as conn:
            user_orders = await Order.get_user_orders(user, conn=conn)
            return web.json_response({'orders': [ Order.order_to_dict(o) for o in user_orders ]})


