import asyncio
from edulafia.database import AsyncSessionLocal
from sqlalchemy import text
from edulafia.core.security import hash_password

async def fix():
    async with AsyncSessionLocal() as session:
        h = hash_password("Admin123!")
        await session.execute(text("UPDATE users SET password_hash = :h WHERE email = 'admin@edulafia.com'"), {"h": h})
        await session.commit()
        print("Fixed password in DB")

if __name__ == "__main__":
    asyncio.run(fix())
