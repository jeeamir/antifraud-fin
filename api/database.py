from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base
from api.config import DATABASE_URL

engine = create_async_engine(DATABASE_URL)

SessionLocal = async_sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
       await db.close()