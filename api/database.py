from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

import os
from dotenv import load_dotenv
load_dotenv()

db_url=os.getenv("DATABASE_URL")

engine = create_async_engine(db_url)

SessionLocal = async_sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
       await db.close()