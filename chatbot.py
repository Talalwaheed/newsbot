"""
chatbot.py
Core chatbot logic using GraphRAG output + Gemini API.
Falls back to direct semantic search if GraphRAG index not ready.
"""
import os
import json
import time
import numpy as np
from pathlib import Path
import google.generativeai as genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AQ.Ab8RN6ITp3beB9smTPMeK4y1sv6nLyWw0piDBJxmjAqBJWwbzg")
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

def load_articles_from_mongo():
    try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        col = client["newsbot"]["articles"]
        articles = list(col.find({"active": True}, {"_id": 0}))
        if articles:
            return articles
    except Exception:
        pass
    return None

def load_articles_from_json():
    paths = ["input/news.json", "news.json"]
    for p in paths:
        if os.path.exists(p):
            with open(p, encoding="utf-8") as f:
                return json.load(f)
    return []

def get_articles():
    articles = load_articles_from_mongo()
    if articles:
        return articles
    return load_articles_from_json()

def load_graphrag_context(query: str) -> str:
    output_dir = Path("output")
    if not output_dir.exists():
        return None
    context_parts = []
    for parquet_file in output_dir.rglob("*.parquet"):
        try:
            import pandas as pd
            df = pd.read_parquet(parquet_file)
            if "title" in df.columns and "summary" in df.columns:
                for _, row in df.iterrows():
                    context_parts.append(f"{row.get('title','')}: {row.get('summary','')}")
        except Exception:
            continue
    if context_parts:
        return "\n".join(context_parts[:20])
    return None

def semantic_search(query: str, articles: list, top_k: int = 5) -> list:
    query_words = set(query.lower().split())
    scored = []
    for a in articles:
        text = f"{a.get('title','')} {a.get('content','')}".lower()
        score = sum(1 for w in query_words if w in text)
        if score > 0:
            scored.append((score, a))
    scored.sort(reverse=True, key=lambda x: x[0])
    return [a for _, a in scored[:top_k]]

def ask(query: str) -> str:
    articles = get_articles()
    if not articles:
        return "No articles found. Please load data first."

    graphrag_context = load_graphrag_context(query)
    relevant = semantic_search(query, articles)
    article_context = "\n\n".join([
        f"Title: {a.get('title','')}\nSource: {a.get('source','')}\nDate: {a.get('published_at','')}\nContent: {a.get('content','')}"
        for a in relevant
    ])

    if graphrag_context:
        context = f"KNOWLEDGE GRAPH CONTEXT:\n{graphrag_context}\n\nRELEVANT ARTICLES:\n{article_context}"
    else:
        context = f"RELEVANT ARTICLES:\n{article_context}"

    prompt = f"""You are a geopolitical news analyst chatbot. Answer the user's question based on the news articles provided.
Be specific, cite article titles when relevant, and be concise.

{context}

USER QUESTION: {query}

ANSWER:"""

    time.sleep(15)
    response = model.generate_content(prompt)
    return response.text

if __name__ == "__main__":
    print("🤖 News Chatbot Ready. Type 'exit' to quit.\n")
    while True:
        q = input("You: ").strip()
        if q.lower() == "exit":
            break
        if q:
            print(f"\nBot: {ask(q)}\n")