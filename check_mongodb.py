import pymongo
import os
from dotenv import load_dotenv

load_dotenv()

mongo_url = os.getenv("MONGO_DB_URL")

print("Mongo URL loaded:", mongo_url is not None)

client = pymongo.MongoClient(mongo_url)

print("Databases:", client.list_database_names())

db = client["KRISHAI"]
print("Collections:", db.list_collection_names())

collection = db["NetworkData"]
print("Document count:", collection.count_documents({}))
