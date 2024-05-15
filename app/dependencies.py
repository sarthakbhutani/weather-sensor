from app.settings import (DB_USERNAME,
DB_PASSWORD,
DB_NAME,
DB_HOST,LOG_LEVEL,SERVICE_NAME,
BASE_ROUTE,
DB_PORT)
from asyncpg import create_pool
import asyncio

async def get_pool():
    print('ass---get_pool')
    pool = await create_pool(user=DB_USERNAME, password=DB_PASSWORD, database=DB_NAME, host=DB_HOST,port=DB_PORT)
    print('---')
    async with pool.acquire() as conn:
        ass = await conn.fetch('SELECT 1')
        print(ass)
    return pool