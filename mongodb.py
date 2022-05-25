import pymongo
from pymongo.mongo_client import MongoClient

# connecting to a local mongoDB instance
my_url = "mongodb://localhost:27017"
client = MongoClient(my_url, serverSelectionTimeoutMS=5000)

db = client["ec_regulation"]
comments = db["comments"]
err_log = db["error_logs"]

# defining db methods
def log_err(page, type, details):
    print(f"exception on page {page}: {type}")
    error = {
        "err_location": f"exception occurred on page {page} (index {page - 1})",
        "err_type": type,
        "err_details": str(details)
    }
    err_log.insert_one(error)

def add_entries(entries, page):
    try:
        comments.insert_many(entries)
        print(f"Inserted entries of page {page} into db")
    except (pymongo.errors.DuplicateKeyError, pymongo.errors.BulkWriteError) as pymoerr:
        log_err(page, "Duplicate key error", pymoerr.details)
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