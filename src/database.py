import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

DATABASE_URL_ASYNC = os.getenv("DATABASE_URL_ASYNC",
                               "postgresql+asyncpg://postgres:admin@localhost:5432/chat_db")

async_engine = create_async_engine(DATABASE_URL_ASYNC, echo=True)
async_session_factory = async_sessionmaker(async_engine)

Base = declarative_base()

async def get_db():
    async with async_session_factory() as session:
        yield session