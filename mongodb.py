import os
import pymongo
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv

load_dotenv()

username = os.environ.get("DBUSER")
password = os.environ.get("DBPASSWORD")
project = os.environ.get("DBPROJECT")

# connections to a mongoDB instance on the cloud and a local one
# my_url = f"mongodb+srv://{username}:{password}@{project}.mongodb.net/?retryWrites=true&w=majority"
my_url = "mongodb://localhost:27017/"
client = MongoClient(my_url, serverSelectionTimeoutMS=5000)

db = client["ec_regulation"]
comments = db["comments"]
err_log = db["error_logs"]

# defining db methods
def log_err(location, type, details):
    print(f"exception on {location}: {type}")
    print(details)
    error = {
        "err_location": f"exception occurred on: {location})",
        "err_type": str(type),
        "err_details": str(details)
    }
    err_log.insert_one(error)

def add_entries(entries, page):
    try:
        comments.insert_many(entries)
        print(f"Inserted entries of page {page} into db")
    except (pymongo.errors.DuplicateKeyError, pymongo.errors.BulkWriteError) as pymoerr:
        log_err(f"loading page {page}", "Duplicate key error", pymoerr.details)
    except Exception as e:
       log_err(page, "Other", e)

def comments_per_page(last_index):
    pipeline=[{ "$group": {"_id" : "$page_index", "comments": { "$push": "$comment_no" } }}]
    pages = list(comments.aggregate(pipeline))
    i = 0
    while i <= last_index:
        try:
            index = list(filter(lambda index: index["_id"] == i, pages))
            if index == []:
                print(f"no page for index {i}")
            i+=1
        except Exception as e:
            print(f"error loading index {i}")
            print(e)
            i+=1