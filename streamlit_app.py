import streamlit as st
import requests

# Backend API URL
API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(page_title="Conversational NL2SQL Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 Conversational NL2SQL Assistant")
st.write("Ask questions in natural language, and I'll generate SQL queries for you.")

# Session state for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Input box
user_input = st.chat_input("Type your query here...")

if user_input:
    # Save user query
    st.session_state["messages"].append({"role": "user", "content": user_input})

    # Call backend
    try:
        response = requests.post(API_URL, json={"query": user_input})
        if response.status_code == 200:
            data = response.json()
            sql_query = data.get("sql_query")
            explanation = data.get("explanation")

            bot_response = ""
            if sql_query:
                bot_response += f"**Generated SQL:**\n```sql\n{sql_query}\n```"
            if explanation:
                bot_response += f"\n\n**Explanation:** {explanation}"

            if not bot_response:
                bot_response = "⚠️ Sorry, I couldn’t generate a SQL query."

            st.session_state["messages"].append({"role": "assistant", "content": bot_response})
        else:
            st.session_state["messages"].append({"role": "assistant", "content": "⚠️ API Error"})
    except Exception as e:
        st.session_state["messages"].append({"role": "assistant", "content": f"⚠️ Backend not reachable: {e}"})


# Render chat messages
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        with st.chat_message("user"):
            st.write(msg["content"])
    else:
        with st.chat_message("assistant"):
            st.write(msg["content"])
