from contextlib import asynccontextmanager
from fastapi import FastAPI
from api.routers import merchants, payers, transactions
from api.kafka_producer import create_kafka_producer

@asynccontextmanager
async def lifespan(app: FastAPI):
    producer = create_kafka_producer()
    try:
        await producer.start()
        app.state.kafka_producer = producer
        yield
    finally:
        await producer.stop()


app = FastAPI(lifespan=lifespan)

app.include_router(merchants.router)
app.include_router(payers.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return { "message": "Hello server"}



