from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

mongo_uri = os.getenv("db_url")
client = AsyncIOMotorClient(mongo_uri)
db = client['ScrappyBot']
