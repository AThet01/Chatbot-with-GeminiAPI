import streamlit as st
import requests
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
# Set Groq API Key
GROQ_API_KEY = os.getenv("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")# Or set in Streamlit secrets

# Check if the key is loaded correctly
if not GROQ_API_KEY:
    print("Error: GROQ_API_KEY not found")
else:
    print("API Key found!")

def get_groq_response(user_input):
    url= "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {"model": "mixtral", "messages": [{"role": "user", "content": user_input}]}

    print("🔵 Sending API Request...")
    print("Headers:", headers)
    print("Payload:", data)

    try:
        response = requests.post(url, json=data, headers=headers)
        print("🟢 Status Code:", response.status_code)
        print("🟢 Response:", response.text)  # Print full response

        response.raise_for_status()  # Raise an error for bad responses
        json_response = response.json()

        if "choices" in json_response and len(json_response["choices"]) > 0:
            return json_response["choices"][0]["message"]["content"]
        else:
            return f"⚠️ Unexpected response format: {json_response}"

    except requests.exceptions.RequestException as e:
        return f"❌ API Error: {e}"


# Streamlit UI
st.title("✈️ Flight Chatbot")
st.write("Ask me about flights!")

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Ask about flights...")
if user_input:
    # Display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get chatbot response
    bot_response = get_groq_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": bot_response})

    # Display bot response
    with st.chat_message("assistant"):
        st.write(bot_response)