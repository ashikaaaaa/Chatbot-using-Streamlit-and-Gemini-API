import os
import streamlit as st
import google.generativeai as genai

# Set your Google API key
os.environ['GOOGLE_API_KEY'] = "AIzaSyDR_vd5ZFjNhIwKD5G3GB-tqd5o8kyR7vE"
GOOGLE_API_KEY = os.environ['GOOGLE_API_KEY']

genai.configure(api_key=GOOGLE_API_KEY)

# Load Gemini Pro model and get responses
geminiModel = genai.GenerativeModel("gemini-pro")
chat = geminiModel.start_chat(history=[])

def get_gemini_response(query):
    
    #Sends the conversation history with the added message and returns the model's response.
    instant_Response = chat.send_message(query, stream=True)
    return instant_Response

def display_chat_history():
    #Displays the chat history stored in the session state.
    
    st.subheader("Chat History")
    for role, text in st.session_state['chat_history']:
        st.markdown(f"**{role}:** {text}")

def main():
    """
    Main function to run the Streamlit app.
    Sets up the page configuration, handles user inputs, and displays the chatbot responses.
    """
    # Page title and sidebar
    st.set_page_config(page_title="Simple Chat Bot", layout="wide")
    st.markdown("# Simple Chat Bot Page")

    # Initialize session state for chat history if it doesn't exist
    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    # Display chat history
    display_chat_history()

    # Chat input
    st.subheader("Start a Conversation")
    input_text = st.text_input("Your Message:", key="input")
    submit_button = st.button("Send")

    if submit_button and input_text:
        output = get_gemini_response(input_text)
        st.session_state['chat_history'].append(("You", input_text))
        for output_chunk in output:
            st.session_state['chat_history'].append(("Bot", output_chunk.text))
            st.markdown(f"**Bot:** {output_chunk.text}")

    # Apply custom CSS for styling
    st.markdown("""
    <style>
        .stButton button {
            background-color: #4CAF50;
            color: white;
        }
        .stTextInput div {
            border-color: #4CAF50;
        }
    </style>
    """, unsafe_allow_html=True)

    # Footer
    st.markdown("""
        <hr>
        <footer>
            <p>Thank You!</p>
        </footer>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
