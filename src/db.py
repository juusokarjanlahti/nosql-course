from pymongo import MongoClient
from bson.objectid import ObjectId

def connect_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["runescape_market"]
    return db

def add_object(db, collection_name, data):
    db[collection_name].insert_one(data)

def update_object(db, collection_name, object_id, data):
    db[collection_name].update_one(
        {"_id": ObjectId(object_id)},
        {"$set": data}
    )

def delete_object(db, collection_name, object_id):
    db[collection_name].delete_one({"_id": ObjectId(object_id)})

def get_objects(db, collection_name):
    return list(db[collection_name].find())