#  Geopolitical News Chatbot

A GraphRAG-powered intelligent chatbot for geopolitical news analysis, built with Microsoft GraphRAG, MongoDB, Google Gemini, and Streamlit.

## Project Overview

This chatbot allows users to ask questions about geopolitical news and receive intelligent, context-aware answers. It uses a knowledge graph built from 100 geopolitical news articles to provide better answers than traditional keyword search.

##  Architecture
news.json (100 articles)
↓
MongoDB (data storage + 24h refresh)
↓
GraphRAG (knowledge graph indexing)
↓
Gemini 2.0 Flash (answer generation)
↓
Streamlit (web chat interface)

##  Tech Stack

| Component | Technology |
|---|---|
| Knowledge Graph | Microsoft GraphRAG |
| Database | MongoDB |
| LLM | Google Gemini 2.0 Flash |
| Embeddings | Gemini Embedding 001 |
| Frontend | Streamlit |
| Language | Python 3.11 |

##  Project Structure
newsbot/
├── app_ui.py          # Streamlit web interface
├── chatbot.py         # Core chatbot logic
├── mongo_loader.py    # MongoDB data loader
├── refresh.py         # 24h auto refresh scheduler
├── settings.yaml      # GraphRAG configuration
├── requirements.txt   # Python dependencies
└── README.md          # This file

##  Setup & Installation

### Prerequisites
- Python 3.11
- MongoDB installed and running
- Google Gemini API key (get free at aistudio.google.com)

### Step 1 — Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Add Your Gemini API Key
Open `chatbot.py` and replace the API key:
```python
GEMINI_API_KEY = "your-gemini-api-key-here"
```

### Step 3 — Load News Data into MongoDB
```bash
python mongo_loader.py
```
This loads all 100 articles into MongoDB and exports txt files for GraphRAG.

### Step 4 — Run GraphRAG Indexing (Optional)
```bash
set GRAPHRAG_API_KEY=your-gemini-api-key-here
set GRAPHRAG_API_BASE=https://generativelanguage.googleapis.com/v1beta/openai/
python -m graphrag.index --root .
```

### Step 5 — Launch the Chatbot
```bash
streamlit run app_ui.py
```

Open browser at `http://localhost:8501`

##  24-Hour Data Refresh

The system automatically refreshes news data every 24 hours:

- New articles are added to MongoDB
- Old articles can be removed
- GraphRAG re-indexes the updated data
- Chatbot answers based on latest news

To manually refresh, click **"Refresh Data Now"** in the sidebar.

To run the auto-refresh scheduler:
```bash
python refresh.py
```

##  Example Questions

- What is happening between Russia and Ukraine?
- Tell me about US and China relations
- What are the latest developments in the Middle East?
- How are sanctions affecting global trade?
- What is happening in South Asia?

##  Features

- ✅ 100 geopolitical news articles indexed
- ✅ MongoDB for dynamic data management
- ✅ GraphRAG knowledge graph for intelligent retrieval
- ✅ Gemini AI for natural language answers
- ✅ 24-hour automatic data refresh
- ✅ Clean web chat interface
- ✅ Add/remove articles dynamically

##  API Keys Required

- **Google Gemini API Key** — Get free at [aistudio.google.com](https://aistudio.google.com/app/apikey)

## 👨‍💻 Author

Muhammad Talal Bin Waheed.
