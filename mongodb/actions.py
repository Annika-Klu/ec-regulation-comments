import pymongo
from utils import current_date_time
from mongodb.setup import db

comments = db["comments"]
err_log = db["error_logs"]

def log_err(location, type, details):
    print(f"exception on {location}: {type}")
    print(details)
    error = {
        "err_location": f"exception occurred on: {location}",
        "err_date_time": current_date_time(),
        "err_type": str(type),
        "err_details": str(details)
    }
    err_log.insert_one(error)

def add_entries(entries, page):
    try:
        comments.insert_many(entries)
        print(f"Inserted entries of page {page} into db")
    except (pymongo.errors.DuplicateKeyError, pymongo.errors.BulkWriteError) as pymoerr:
        log_err(f"inserting page {page}", "Duplicate key error", pymoerr.details)
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