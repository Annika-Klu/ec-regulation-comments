from pymongo.mongo_client import MongoClient

# connecting to a local mongoDB instance
my_url = "mongodb://localhost:27017"
client = MongoClient(my_url, serverSelectionTimeoutMS=5000)

db = client["ec_regulation"]
col = db["comments"]

# defining db method
def add_entries(entries, page):
    try:
        col.insert_many(entries)
        print(f"inserted entries of page {page} into db")
    except Exception as e:
        print(e.details)