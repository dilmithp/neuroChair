from pymongo import MongoClient
import os
import datetime

# MongoDB Connection
# Using the connection string from requirements: mongodb://mongodb:27017/neurochair
# Fallback to localhost if not in docker for local testing
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/neurochair")
DB_NAME = "neurochair"

def get_db():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME]

def get_sensor_data_collection():
    db = get_db()
    return db["sensor_data"]

def get_recent_sensor_data(limit=1):
    """Get the most recent sensor data entries."""
    collection = get_sensor_data_collection()
    return list(collection.find().sort("timestamp", -1).limit(limit))

def get_historical_data(hours=24):
    """Get sensor data for the last n hours."""
    collection = get_sensor_data_collection()
    start_time = datetime.datetime.now() - datetime.timedelta(hours=hours)
    return list(collection.find({"timestamp": {"$gte": start_time}}).sort("timestamp", 1))
