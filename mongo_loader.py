"""
mongo_loader.py
Loads news.json into MongoDB and exports txt files for GraphRAG.
Run once to initialize, then run refresh.py every 24h.
"""
import json
import os
from datetime import datetime
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "newsbot"
COLLECTION = "articles"
INPUT_DIR = "input"

def connect():
    client = MongoClient(MONGO_URI)
    return client[DB_NAME][COLLECTION]

def load_json_to_mongo(json_path="input/news.json"):
    col = connect()
    with open(json_path, encoding="utf-8") as f:
        articles = json.load(f)
    col.delete_many({})  # clear old
    for a in articles:
        a["loaded_at"] = datetime.utcnow()
        a["active"] = True
    col.insert_many(articles)
    print(f"✅ Loaded {len(articles)} articles into MongoDB")
    return articles

def export_to_txt():
    col = connect()
    articles = list(col.find({"active": True}))
    os.makedirs(INPUT_DIR, exist_ok=True)
    # Remove old txt files
    for f in os.listdir(INPUT_DIR):
        if f.endswith(".txt"):
            os.remove(os.path.join(INPUT_DIR, f))
    for i, a in enumerate(articles):
        path = os.path.join(INPUT_DIR, f"article_{i}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"{a.get('title','')}\n\n{a.get('content','')}")
    print(f"✅ Exported {len(articles)} txt files for GraphRAG")

def add_article(article: dict):
    col = connect()
    article["loaded_at"] = datetime.utcnow()
    article["active"] = True
    col.insert_one(article)
    print(f"✅ Added article: {article.get('title','')}")

def remove_article(title: str):
    col = connect()
    col.update_one({"title": title}, {"$set": {"active": False}})
    print(f"✅ Removed article: {title}")

if __name__ == "__main__":
    load_json_to_mongo()
    export_to_txt()
