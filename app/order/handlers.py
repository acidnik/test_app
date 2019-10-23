from aiohttp import web
import json

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


    @login_required
    async def place_orders(request):
        """
            curl -d '[{"book_id": 1, "shop_id": 1, "amount": 1}]' -H 'Authorization: xxxxx'
            returns list of created orders

            if order for this user with this book_id/shop_id already exists - increases amount
            returns list of orders
        """
        try:
            json_text = await request.text()
            data = json.loads(json_text)
            for o in data:
                if o['amount'] <= 0:
                    raise ValueError
        except (json.JSONDecodeError, ValueError):
            logging.error(f"bad json {json_text}")
            raise web.HTTPBadRequest

        async with request.app['db'].acquire() as conn:
            try:
                order_res = await Order.place_orders(orders_list=data, user_id=request['user'].id, conn=conn)
            except:
                logging.exception(f"error in input data")
                raise web.HTTPBadRequest
        return web.json_response({'orders': [ Order.order_to_dict(o) for o in order_res ]})
