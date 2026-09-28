from aiokafka import AIOKafkaConsumer
from api import models
from api.config import KAFKA_BOOTSTRAP_SERVERS
import asyncio
import json
from decimal import Decimal
from uuid import UUID
from api.database import SessionLocal
from consumer.scoring import is_fraud_by_rules
from api.models import TransactionStatus


async def save_transaction(transaction_data):
    transaction_id = UUID(transaction_data["id"])

    async with SessionLocal() as db:
        existing_transaction = await db.get(
            models.Transaction,
            transaction_id
        )

        if existing_transaction is not None:
            return False

        amount = Decimal(transaction_data["amount"])
        is_fraud = is_fraud_by_rules(amount)

        transaction = models.Transaction(
            id=transaction_id,
            payer_id=UUID(transaction_data["payer_id"]),
            merchant_id=UUID(transaction_data["merchant_id"]),
            amount=amount,
            currency=transaction_data["currency"],
            status=TransactionStatus.SCORED,
            is_fraud=is_fraud
        )

        db.add(transaction)

        try:
            await db.commit()
            return True
        except Exception:
            await db.rollback()
            raise



async def consume():
    consumer = AIOKafkaConsumer(
        'transactions_raw',
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        group_id='antifraud-scoring',
        auto_offset_reset='earliest',
        value_deserializer=lambda value: json.loads(
            value.decode('utf-8')
        ),
        enable_auto_commit=False
    )



    try:
        await consumer.start()
        async for msg in consumer:
            was_created = await save_transaction(msg.value)
            await consumer.commit()

            if was_created:
                print(
                f"Saved transaction: {msg.value['id']}, "
                f"topic: {msg.topic}, "
                f"partition: {msg.partition}, "
                f"offset: {msg.offset}")
            else:
                print(f"Already existed transaction: {msg.value['id']}, ")

    finally:
        await consumer.stop()

if __name__ == "__main__":
    asyncio.run(consume())