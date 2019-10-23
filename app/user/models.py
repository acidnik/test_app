from app.db import users, sessions, books, shops, orders
from app.user.utils import hash_password
from app.session.models import Session
from sqlalchemy.sql import select, and_
import logging

class User:
    @classmethod
    async def auth(cls, login: str, password: str, conn):
        cursor = await conn.execute(select([users]).where(and_(users.c.login == login, users.c.password == hash_password(password))))
        user = await cursor.fetchone()
        if user:
            session = await Session.create(user, conn=conn)
            return session

        return None

    @classmethod
    async def get_by_id(cls, user_id: int, conn):
        cursor = await conn.execute(select([users]).where(users.c.id == user_id))
        user = await cursor.fetchone()
        return user

    @classmethod
    def to_dict(cls, user):
        return {
            'user_id': user.id,
            'login': user.login,
            'email': user.email,
        }

    @classmethod
    async def get_by_session_key(cls, session_key: str, conn):
        cursor = await conn.execute(select([users, sessions.c.session_key]).select_from(sessions.join(users)).where(sessions.c.session_key == session_key))
        user = await cursor.fetchone()
        return user

    @classmethod
    def order_to_dict(cls, order):
        return {
            'book': {
                'id': order['books_id'],
                'author': order['books_author'],
                'title': order['books_title'],
            },
            'shop': {
                'id': order['shops_id'],
                'name': order['shops_name'],
            },
            'id': order['orders_id'],
            'amount': order['orders_amount'],
        }

    @classmethod
    async def orders(cls, user, conn):
        cursor = await conn.execute(
            select([users, orders, books, shops], use_labels=True)
            .select_from(users.join(orders).join(shops).join(books))
            .where(users.c.id == user.id)
        )
        rows = await cursor.fetchall()
        return rows

