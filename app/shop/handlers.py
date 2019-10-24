from aiohttp import web

from app.shop.models import Shop

import logging

class ShopHandlers:
    def __init__(self):
        pass

    async def list_books(request):
        """
        отобразить ассортиметн магазина
        не требует авторизации
        """
        app = request.app
        try:
            shop_id = int(request.match_info['shop_id'])
        except ValueError:
            raise web.HTTPBadRequest
        async with app['db'].acquire() as conn:
            books = await Shop.list_books(shop_id, conn=conn)
        return web.json_response({'books': [ Shop.book_to_dict(b) for b in books ]})

