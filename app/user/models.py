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
        self.session_key = kwargs['session_key']

    @classmethod
    async def auth(cls, login: str, password: str, conn):
        cursor = await conn.execute(select([users]).where(and_(users.c.login == login, users.c.password == hash_password(password))))
        user = await cursor.fetchone()
        if user:
            logging.info(f"GOT {dict(user)}")
            session = await Session.create(user, conn=conn)
            return session
        else:
            logging.info(f"NONE for {login} / {password}")

        return None

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

