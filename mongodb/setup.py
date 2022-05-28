import os
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

load_dotenv()

username = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
project = os.environ.get("DB_PROJECT")
environment = os.environ.get("DB_HOST")

# connections to a local mongoDB instance or one on the cloud
if environment == "local":
    my_url = "mongodb://localhost:27017/"
else:
    my_url = f"mongodb+srv://{username}:{password}@{project}.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(my_url, serverSelectionTimeoutMS=5000)
db = client["ec_regulation"]