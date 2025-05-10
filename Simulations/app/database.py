import asyncpg

DATABASE_URL = "postgresql://user:password@db:5432/simulations_db"

async def get_db():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()
