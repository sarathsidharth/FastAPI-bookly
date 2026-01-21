from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlalchemy import text
from src.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True
)

async def init_db():
    async with engine.begin() as conn:
        # result = await conn.execute(text("SELECT 'hello';"))
        # print(result.all())
        from src.books.models import Book

        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session()->AsyncSession:
    Session=sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False
    )

    async with Session() as session:
        yield session
# async def get_session() -> AsyncSession:
#     async with async_session_maker() as session:
#         yield session