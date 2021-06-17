from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from diaboli_mundi_back.settings import settings


class MongoDB:
    db: AsyncIOMotorDatabase = None


mongo = MongoDB()


def create_mongo_conn() -> None:
    if mongo.db is None:
        mongo_client: AsyncIOMotorClient = AsyncIOMotorClient(settings.mongodb_url)
        mongo.db: AsyncIOMotorDatabase = mongo_client.get_database()


def close_mongo_conn() -> None:
    if mongo.db:
        mongo.db.client.close()
        mongo.db = None


def get_mongo() -> AsyncIOMotorDatabase:
    return mongo.db


def ensure_mongo() -> AsyncIOMotorDatabase:
    create_mongo_conn()
    return get_mongo()
