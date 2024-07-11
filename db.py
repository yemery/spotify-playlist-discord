from pymongo import MongoClient 
from config import *

def get_db_connection():
    try:
        client = MongoClient(MONGO_URI)
        print("Connected to the database")
        return client[MONGO_DB]
    except Exception as e:
        print("Error in connecting to the database")
        print(e)
        return None

    
