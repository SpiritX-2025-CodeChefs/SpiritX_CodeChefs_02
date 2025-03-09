from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI
import os

# Database configuration
MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = "cricket_fantasy"

client = None
db = None


async def connect_to_mongodb():
    """Connect to MongoDB."""
    global client, db
    client = AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]

    # Create indexes
    await db.users.create_index("username", unique=True)
    await db.sessions.create_index("session_id", unique=True)
    await db.players.create_index("id", unique=True)


async def close_mongodb_connection():
    """Close MongoDB connection."""
    global client
    if client:
        client.close()


def get_db():
    """Get database instance."""
    return db


def init_app(app: FastAPI):
    """Initialize database connection on app startup."""
    app.add_event_handler("startup", connect_to_mongodb)
    app.add_event_handler("shutdown", close_mongodb_connection)
