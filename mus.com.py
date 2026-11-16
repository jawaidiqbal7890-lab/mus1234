import os
from google import genai
from google.genai import types

# 1. Initialize the client
# Make sure GEMINI_API_KEY is set in your environment variables:
# export GEMINI_API_KEY="your-api-key-here"
client = genai.Client()

# 2. Define the system instructions to enforce the 3-stage structure and identity
system_instruction = """
You are "AI Master", an advanced and helpful AI assistant. 
For every query or prompt given by the user, you MUST format your answer into strictly three stages:

Stage 1: Explanation
- Thoroughly explain the concepts, background, or context behind the user's question or problem.

Stage 2: Solution
- Provide a clear, actionable, step-by-step solution, code, or answer to address the request directly.

Stage 3: AI Master Summary
- Give a concise takeaway, key recommendation, or high-level summary of the solution.

Always introduce yourself as AI Master when appropriate, and remain clear, structured, and helpful.
"""

def ask_ai_master(prompt: str):
    """Sends a user query to AI Master and prints the 3-stage response."""
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                temperature=0.7,
            )
        )
        print(f"\n--- AI Master Response ---\n")
        print(response.text)
        print("\n" + "="*40 + "\n")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- Interactive Terminal Loop ---
if __name__ == "__main__":
    print("Welcome to AI Master! Ask me anything (type 'exit' or 'quit' to stop).\n")
    
    while True:
        user_input = input("You: ")
        if user_input.strip().lower() in ['exit', 'quit']:
            print("AI Master signing off. Goodbye!")
            break
        
        if not user_input.strip():
            continue
            
        ask_ai_master(user_input)
