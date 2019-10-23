from app.db import users, sessions
from app.user.utils import hash_password
from app.session.models import Session
from sqlalchemy.sql import select, and_
import logging

class User:
    def __init__(self, **kwargs):
        self.user_id = kwargs['user_id']
        self.login = kwargs['login']
        self.password = kwargs['password']
        self.session_key = kwargs.get('session_key')
        self.email = kwargs['email']

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
        if not user:
            return None
        user = dict(user)
        user['user_id'] = user['id']
        # return None
        return cls(**user)

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
        }

    @classmethod
    async def get_by_session_key(cls, session_key: str, conn):
        cursor = await conn.execute(select([users, sessions.c.session_key]).select_from(sessions.join(users)).where(sessions.c.session_key == session_key))
        user = await cursor.fetchone()
        if not user:
            return None
        user = dict(user)
        user['user_id'] = user['id']
        # return None
        return cls(**user)

