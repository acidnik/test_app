import uuid

class Session:
    @classmethod
    async def create(cls, user, redis):
        session_key = str(uuid.uuid4())
        await redis.set(session_key, str(user['id']))
        return session_key

    @classmethod
    async def delete(cls, session_key, redis):
        await redis.delete([session_key])

    @classmethod
    async def get(cls, session_key, redis):
        res = await redis.get(session_key)
        if res:
            return int(res)
        return None



