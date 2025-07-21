from motor.motor_asyncio import AsyncIOMotorClient
from app.config import settings

class Database:
    client: AsyncIOMotorClient = None
    database = None

db = Database()

async def connect_to_mongo():
    db.client = AsyncIOMotorClient(settings.mongodb_url)
    db.database = db.client[settings.mongodb_db]
    print(f"Connected to MongoDB: {settings.mongodb_db}")

async def close_mongo_connection():
    if db.client:
        db.client.close()
        print("MongoDB connection closed")

def get_collection(collection_name: str):
    return db.database[collection_name]