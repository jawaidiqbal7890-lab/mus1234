
import streamlit as st
from google import genai
from google.genai import types

# Page configuration
st.set_page_config(
    page_title="AI Master",
    page_icon="🤖",
    layout="centered"
)

# AI Master system instructions
system_instruction = """
You are AI Master, an advanced and helpful AI assistant.

For every query, format your answer into three stages:

Stage 1: Explanation
Explain the concepts and background.

Stage 2: Solution
Provide a clear, actionable, step-by-step answer.

Stage 3: AI Master Summary
Give a concise summary and key recommendation.

Always introduce yourself as AI Master when appropriate.
Remain clear, structured, and helpful.
"""

# App heading
st.title("🤖 AI Master")
st.caption("Your personal AI assistant powered by Google Gemini")

# Load Gemini API key from Streamlit Secrets
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
except Exception:
    st.error("Gemini API key is missing. Please configure Streamlit Secrets.")
    st.stop()

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
prompt = st.chat_input("Ask AI Master anything...")

if prompt:
    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("AI Master is thinking..."):
            try:
                # Include conversation history
                history = [
                    {
                        "role": "user" if m["role"] == "user" else "model",
                        "parts": [{"text": m["content"]}]
                    }
                    for m in st.session_state.messages
                ]

                response = client.models.generate_content(
                    model="gemhini-3.8-flas",
                    contents=history,
                    config=types.GenerateContentConfig(
                        system_instruction=system_instruction,
                        temperature=0.7,
                    )
                )

                answer = response.text

                if not answer:
                    answer = "Sorry, I couldn't generate a response. Please try again."

                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                st.error(f"An error occurred: {e}")
