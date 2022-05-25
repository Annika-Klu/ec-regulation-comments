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
        print(e)
        with open('error_logs.txt', 'w') as log:
            log.write(f"an exception occurred on page {page} (index {page - 1})")
            log.write(str(e))
            log.close()

def comments_per_page(last_index):
    pipeline=[{ "$group": {"_id" : "$page_index", "comments": { "$push": "$comment_no" } }}]
    pages = list(col.aggregate(pipeline))
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