from app.db import sessions
import uuid

class Session:
    @classmethod
    async def create(cls, user, conn):
        session_key = str(uuid.uuid4())
        await conn.execute(sessions.insert().values([{'user_id': user['id'], 'session_key': session_key }]))
        return session_key

    @classmethod
    async def delete(cls, session_key, conn):
        pass
        # await conn.execute(sessions.delete().where(sessions.c.session_key == session_key))

