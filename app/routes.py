from aiohttp import web

from app.user.handlers import UserHandlers
from app.order.handlers import OrderHandlers
from app.shop.handlers import ShopHandlers


def add_routes(router):
    user = UserHandlers
    order = OrderHandlers
    shops = ShopHandlers
    router.add_routes([
        web.get('/api/v1/user/login', user.login),
        web.post('/api/v1/user/logout', user.logout),
        web.get('/api/v1/user/{user_id:\d+}', user.get),

        web.get('/api/v1/orders', order.orders),
        web.post('/api/v1/orders', order.place_orders),
        
        web.get('/api/v1/shop/{shop_id:\d+}', shops.list_books),
    ])

