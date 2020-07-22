from pymongo import MongoClient

def read_from_mongo():
    MONGO_URL = "mongodb://localhost:27017"
    MONGO_DB = "web_crawler"
    MONGO_TABLE = "comments"

    client = MongoClient(MONGO_URL)  # 生成mongodb对象
    collection = client[MONGO_DB][MONGO_TABLE]
    all_results = collection.find()
    data = []
    for res in all_results:
        data.append(res)
    return data

if __name__ == '__main__':
    data = read_from_mongo()
    comments = set()
    for d in data:
        comments.add(d['comment'])
    print(len(list(comments)))
