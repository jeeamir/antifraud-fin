from fastapi import FastAPI
from api.routers import merchants, payers, transactions

app = FastAPI()

app.include_router(merchants.router)
app.include_router(payers.router)
app.include_router(transactions.router)

@app.get("/")
async def root():
    return { "message": "Hello server"}



