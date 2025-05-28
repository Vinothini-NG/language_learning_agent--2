import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
import os
import random

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-flash")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hey! Ready to polish your English? Type something or pick a prompt below! 😎"}
    ]

if "feedback" not in st.session_state:
    st.session_state.feedback = {}

if "learning_preferences" not in st.session_state:
    st.session_state.learning_preferences = {
        "mode": "Everything",
        "difficulty": "Intermediate",
        "show_alternatives": True,
        "detailed_explanations": True
    }

if "chat_active" not in st.session_state:
    st.session_state.chat_active = True

# CSS for colored text
st.markdown("""
<style>
.user-text { color: #FFA500; font-weight: bold; }
.corrected-text { color: #008000; font-weight: bold; }
.assistant-text { color: #1E90FF; }
</style>
""", unsafe_allow_html=True)

# Conversational responses
def get_conversational_response(text):
    text_lower = text.lower().strip()
    greetings = ["Hey! What's up? 😊", "Hi! Let's make your English shine! 🌟"]
    farewells = ["See ya! Keep practicing! 👋", "Bye! Come back soon! 😄"]
    questions = ["Cool question! Let's polish it. 🤔", "Nice one! Let's tweak it. 😎"]
    general = ["Got it! Let's make it better. 💬", "Awesome! Here's a smoother version. 😊"]

    if any(word in text_lower for word in ['hi', 'hello', 'hey']):
        return random.choice(greetings)
    elif any(word in text_lower for word in ['bye', 'goodbye', 'see ya']):
        return random.choice(farewells)
    elif '?' in text_lower:
        return random.choice(questions)
    return random.choice(general)

# Generate follow-up question using Gemini API
def generate_follow_up_question(text):
    try:
        prompt = f"Based on this user input: '{text}', generate a short follow-up question in one sentence to continue the conversation."
        response = model.generate_content(prompt)
        return response.text.strip() or "What else would you like to talk about?"
    except Exception as e:
        return "What else would you like to talk about?"

# Generate a direct response to the user's input using Gemini API
def generate_direct_response(text):
    try:
        prompt = f"Respond directly to this user input in one sentence, considering the current date and time is 07:18 PM IST on Tuesday, May 27, 2025: '{text}'"
        response = model.generate_content(prompt)
        return response.text.strip() or "I'm not sure how to respond to that."
    except Exception as e:
        return f"Error: {str(e)}"

# Process text with Gemini API
def process_with_gemini(text, task):
    try:
        if task == "grammar":
            prompt = f"Correct the grammar of this text and return only the corrected version: '{text}'"
            response = model.generate_content(prompt)
            return response.text.strip() or text
        elif task == "vocabulary":
            prompt = f"Suggest 2-3 synonyms for key words in this text: '{text}'"
            response = model.generate_content(prompt)
            return response.text.strip() or "No synonyms suggested."
        elif task == "explanation":
            prompt = f"Explain in one sentence why the grammar in '{text}' was corrected to '{st.session_state.corrected_text}'."
            response = model.generate_content(prompt)
            return response.text.strip() or "No explanation available."
    except Exception as e:
        return f"Error: {str(e)}"

# Main text processing
def process_text(text, mode, difficulty, show_alternatives, detailed_explanations):
    if not text or len(text.strip()) < 3:
        return "Type a full sentence or question, and I'll help! 😊"

    response = f"<span class='assistant-text'>{get_conversational_response(text)}</span>\n\n"
    corrected_text = process_with_gemini(text, "grammar")
    st.session_state.corrected_text = corrected_text  # Store for explanation
    response += f"<span class='user-text'>Your text</span>: {text}\n\n<span class='corrected-text'>Polished version</span>: {corrected_text}\n\n"

    if difficulty in ["Advanced", "Professional"]:
        response += "I used a sharper style for your level! 💪\n\n"
    elif difficulty == "Beginner":
        response += "I kept it simple for you! 😊\n\n"

    if mode in ["Everything", "Grammar Only"] and detailed_explanations:
        explanation = process_with_gemini(text, "explanation")
        response += f"<span class='assistant-text'>Why?</span> {explanation}\n\n"

    if mode in ["Everything", "Vocabulary Building"] and show_alternatives:
        vocab = process_with_gemini(corrected_text, "vocabulary")
        response += f"<span class='assistant-text'>Word alternatives</span>:\n{vocab}\n\n"

    # Add direct response to the user's input
    direct_response = generate_direct_response(corrected_text)
    response += f"<span class='assistant-text'>My answer</span>: {direct_response}\n\n"

    follow_up = generate_follow_up_question(corrected_text)
    response += f"<span class='assistant-text'>{follow_up}</span>"
    return response

def main():
    st.title("English Learning Buddy 😎")
    st.subheader("Chat, fix, and learn English fast!")

    # Sidebar for preferences
    with st.sidebar:
        st.header("Your Settings")
        mode = st.selectbox("Focus:", ["Everything", "Grammar Only", "Vocabulary Building"])
        difficulty = st.select_slider("Level:", ["Beginner", "Intermediate", "Advanced", "Professional"])
        show_alternatives = st.toggle("Show synonyms", True)
        detailed_explanations = st.toggle("Explain changes", True)

        st.session_state.learning_preferences.update({
            "mode": mode,
            "difficulty": difficulty,
            "show_alternatives": show_alternatives,
            "detailed_explanations": detailed_explanations
        })

        if st.button("Clear Chat"):
            st.session_state.messages = [
                {"role": "assistant", "content": "Hey! Ready to polish your English? Type something or pick a prompt below! 😎"}
            ]
            st.session_state.feedback = {}
            st.session_state.chat_active = True
            st.rerun()

    # Prompt choice box
    st.markdown("**Quick Prompts**")
    prompt = st.selectbox("Try a sample sentence:", [
        "Select a prompt...",
        "I go to school yesterday.",
        "She don't like coffee.",
        "How to improve my English?",
        "Hello, how you are?"
    ], key="prompt_select")
    if prompt != "Select a prompt..." and st.button("Use This Prompt"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.chat_active = True
        st.rerun()

    # Chat interface
    for idx, message in enumerate(st.session_state.messages):
        with st.chat_message(message["role"]):
            st.markdown(message["content"], unsafe_allow_html=True)
            if message["role"] == "assistant" and st.session_state.chat_active:
                cols = st.columns(4)
                with cols[0]:
                    if st.button("👍 Helpful", key=f"helpful_{idx}"):
                        st.session_state.feedback[str(idx)] = True
                        st.rerun()
                with cols[1]:
                    if st.button("🔄 Correct Again", key=f"retry_{idx}"):
                        user_msg = next((msg["content"] for msg in reversed(st.session_state.messages[:idx]) if msg["role"] == "user"), "")
                        st.session_state.messages = st.session_state.messages[:idx]
                        st.session_state.messages.append({"role": "user", "content": user_msg})
                        st.rerun()
                with cols[2]:
                    if st.button("📚 Suggest Synonyms", key=f"synonyms_{idx}"):
                        user_msg = next((msg["content"] for msg in reversed(st.session_state.messages[:idx]) if msg["role"] == "user"), "")
                        if user_msg:
                            vocab = process_with_gemini(user_msg, "vocabulary")
                            follow_up = generate_follow_up_question(user_msg)
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": f"<span class='assistant-text'>Word alternatives</span>:\n{vocab}\n\n<span class='assistant-text'>{follow_up}</span>"
                            })
                        st.rerun()
                with cols[3]:
                    if st.button("Next Topic", key=f"next_topic_{idx}"):
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": "<span class='assistant-text'>Let's switch gears! What's your favorite hobby? 😊</span>"
                        })
                        st.rerun()

    # End Chat button
    if st.session_state.chat_active:
        if st.button("End Chat"):
            st.session_state.chat_active = False
            st.session_state.messages.append({
                "role": "assistant",
                "content": "<span class='assistant-text'>Thanks for chatting! See you next time! 👋</span>"
            })
            st.rerun()
    else:
        st.markdown("<span class='assistant-text'>Chat ended. Start a new one using the Clear Chat button in the sidebar!</span>", unsafe_allow_html=True)

    # User input
    if st.session_state.chat_active:
        user_text = st.chat_input("Type your text or pick a prompt above! 💬")
        if user_text:
            st.session_state.messages.append({"role": "user", "content": user_text})
            with st.chat_message("user"):
                st.markdown(f"<span class='user-text'>{user_text}</span>", unsafe_allow_html=True)
            with st.spinner("Polishing... ✨"):
                response = process_text(
                    user_text,
                    st.session_state.learning_preferences["mode"],
                    st.session_state.learning_preferences["difficulty"],
                    st.session_state.learning_preferences["show_alternatives"],
                    st.session_state.learning_preferences["detailed_explanations"]
                )
            st.session_state.messages.append({"role": "assistant", "content": response})
            with st.chat_message("assistant"):
                st.markdown(response, unsafe_allow_html=True)

if __name__ == "__main__":
    main()