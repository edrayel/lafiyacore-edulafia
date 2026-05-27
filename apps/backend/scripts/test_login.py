import asyncio
from edulafia.modules.auth.service import AuthService
from edulafia.database import AsyncSessionLocal

from edulafia.modules.auth.repository import AuthRepository

async def test():
    async with AsyncSessionLocal() as session:
        repo = AuthRepository(session)
        service = AuthService(repo)
        user = await service.login("admin@edulafia.com", "Admin123!")
        print(user)

if __name__ == "__main__":
    asyncio.run(test())
