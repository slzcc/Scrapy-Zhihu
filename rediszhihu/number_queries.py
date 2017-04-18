from pymongo import MongoClient
import os
MONGODB_HOST = os.getenv('MONGODB_DB_HOST')
MONGODB_PORT = int(os.getenv('MONGODB_DB_PORT'))

conn = MongoClient(MONGODB_HOST, MONGODB_PORT)

db = conn.zhihu

print(db.user_information.find().count())
