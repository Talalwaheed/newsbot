"""
app_ui.py
Streamlit web UI for the News GraphRAG Chatbot.
Run with: streamlit run app_ui.py
"""
import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(__file__))
from chatbot import ask, get_articles

# Page config
st.set_page_config(
    page_title="News GraphRAG Chatbot",
    page_icon="🌍",
    layout="wide"
)

# Sidebar
with st.sidebar:
    st.title("🌍 News Chatbot")
    st.markdown("**Powered by GraphRAG + Gemini**")
    st.divider()

    # Stats
    articles = get_articles()
    st.metric("Articles in DB", len(articles))

    st.divider()
    st.markdown("### Data Source")
    try:
        from pymongo import MongoClient
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.server_info()
        st.success("✅ MongoDB Connected")
    except Exception:
        st.warning("⚠️ MongoDB offline\nUsing JSON fallback")

    import pathlib
    if pathlib.Path("output").exists():
        st.success("✅ GraphRAG Index Ready")
    else:
        st.warning("⚠️ GraphRAG indexing pending")

    st.divider()
    st.markdown("### 24h Refresh")
    if st.button("🔄 Refresh Data Now"):
        try:
            from mongo_loader import load_json_to_mongo, export_to_txt
            load_json_to_mongo()
            export_to_txt()
            st.success("Data refreshed!")
        except Exception as e:
            st.error(f"Error: {e}")

# Main chat area
st.title("🌍 Geopolitical News Chatbot")
st.caption("Ask anything about the latest geopolitical news")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.messages.append({
        "role": "assistant",
        "content": "Hello! I'm your geopolitical news analyst. Ask me anything about current world events, conflicts, diplomacy, or international relations."
    })

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if prompt := st.chat_input("Ask about world news..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing news graph..."):
            response = ask(prompt)
        st.markdown(response)

    st.session_state.messages.append({"role": "assistant", "content": response})
