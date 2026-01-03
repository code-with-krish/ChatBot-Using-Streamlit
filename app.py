# ==============================
# LLM PART (UNCHANGED)
# ==============================
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

import streamlit as st
from dotenv import load_dotenv
import os
from PIL import Image

load_dotenv()

llm = ChatOpenAI(
    model="xiaomi/mimo-v2-flash:free",
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7
)

# ==============================
# PAGE CONFIG
# ==============================
st.set_page_config(
    page_title="Kronetic",
    page_icon="🤖",
    layout="wide"
)

# ==============================
# PROFESSIONAL CHATBOT UI CSS
# ==============================
st.markdown("""
<style>
/* Import Professional Font */
@import url('https://fonts.googleapis.com/css2?family=SF+Pro+Display:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap');

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main Background */
.stApp {
    background: #0f172a;
}

/* Top Navigation Bar */
.top-nav {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    height: 60px;
    background: rgba(15, 23, 42, 0.95);
    backdrop-filter: blur(10px);
    border-bottom: 1px solid rgba(148, 163, 184, 0.1);
    display: flex;
    align-items: center;
    padding: 0 24px;
    z-index: 1000;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.nav-content {
    max-width: 1200px;
    margin: 0 auto;
    width: 100%;
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo-circle {
    width: 36px;
    height: 36px;
    border-radius: 8px;
    background: linear-gradient(135deg, #3b82f6, #2563eb);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.3);
}

.nav-title {
    font-size: 18px;
    font-weight: 600;
    color: #f8fafc;
    letter-spacing: -0.3px;
}

/* Chat Container */
.chat-container {
    max-width: 800px;
    margin: 80px auto 100px;
    padding: 0 20px;
    min-height: calc(100vh - 180px);
}

/* Welcome Message */
.welcome-card {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 16px;
    padding: 40px;
    text-align: center;
    margin-bottom: 30px;
}

.welcome-card h1 {
    font-size: 32px;
    font-weight: 700;
    color: #f8fafc;
    margin-bottom: 12px;
}

.welcome-card p {
    font-size: 16px;
    color: #94a3b8;
    margin: 0;
}

/* Message Styling */
.stChatMessage {
    background: transparent !important;
    padding: 16px 0 !important;
}

/* User Message */
[data-testid="stChatMessageContent"]:has(+ [data-testid="stChatMessageAvatar"]) {
    background: #3b82f6 !important;
    color: #ffffff !important;
    border-radius: 16px !important;
    padding: 12px 16px !important;
    margin-left: auto !important;
    max-width: 80% !important;
    box-shadow: 0 2px 8px rgba(59, 130, 246, 0.2) !important;
    font-size: 15px !important;
    line-height: 1.5 !important;
}

/* Assistant Message */
[data-testid="stChatMessageContent"] {
    background: rgba(30, 41, 59, 0.6) !important;
    color: #f8fafc !important;
    border: 1px solid rgba(148, 163, 184, 0.1) !important;
    border-radius: 16px !important;
    padding: 12px 16px !important;
    max-width: 80% !important;
    font-size: 15px !important;
    line-height: 1.6 !important;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
}

/* Chat Input Container */
.stChatInputContainer {
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    background: rgba(15, 23, 42, 0.95) !important;
    backdrop-filter: blur(10px) !important;
    border-top: 1px solid rgba(148, 163, 184, 0.1) !important;
    padding: 16px 0 !important;
    z-index: 999 !important;
}

/* Chat Input */
[data-testid="stChatInput"] {
    max-width: 800px !important;
    margin: 0 auto !important;
    background: rgba(30, 41, 59, 0.8) !important;
    border: 1px solid rgba(148, 163, 184, 0.2) !important;
    border-radius: 24px !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1) !important;
}

[data-testid="stChatInput"] textarea {
    background: transparent !important;
    color: #f8fafc !important;
    font-size: 15px !important;
    padding: 14px 20px !important;
    border: none !important;
}

[data-testid="stChatInput"] textarea::placeholder {
    color: #64748b !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
}

/* Send Button */
[data-testid="stChatInput"] button {
    background: #3b82f6 !important;
    color: white !important;
    border-radius: 50% !important;
    padding: 8px !important;
    transition: all 0.2s ease !important;
}

[data-testid="stChatInput"] button:hover {
    background: #2563eb !important;
    transform: scale(1.05) !important;
}

/* Exit Button */
.exit-button {
    position: fixed;
    top: 14px;
    right: 24px;
    z-index: 1001;
}

.exit-button button {
    background: rgba(239, 68, 68, 0.1) !important;
    color: #ef4444 !important;
    border: 1px solid rgba(239, 68, 68, 0.2) !important;
    border-radius: 8px !important;
    padding: 8px 16px !important;
    font-size: 14px !important;
    font-weight: 500 !important;
    transition: all 0.2s ease !important;
    height: 36px !important;
}

.exit-button button:hover {
    background: rgba(239, 68, 68, 0.2) !important;
    border-color: #ef4444 !important;
}

/* Spinner */
.stSpinner > div {
    border-color: #3b82f6 transparent transparent transparent !important;
}

/* Exit Screen */
.exit-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    min-height: 100vh;
    background: #0f172a;
    animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

.exit-screen h1 {
    font-size: 48px;
    font-weight: 700;
    color: #f8fafc;
    text-align: center;
    margin: 0;
    line-height: 1.3;
}

.exit-screen .brand {
    color: #3b82f6;
    display: block;
    margin-top: 8px;
}

/* Footer */
.footer {
    position: fixed;
    bottom: 80px;
    left: 50%;
    transform: translateX(-50%);
    color: #64748b;
    font-size: 13px;
    font-weight: 500;
    z-index: 998;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 6px;
}

::-webkit-scrollbar-track {
    background: rgba(30, 41, 59, 0.3);
}

::-webkit-scrollbar-thumb {
    background: rgba(148, 163, 184, 0.3);
    border-radius: 3px;
}

::-webkit-scrollbar-thumb:hover {
    background: rgba(148, 163, 184, 0.5);
}

/* Responsive */
@media (max-width: 768px) {
    .chat-container {
        padding: 0 16px;
    }
    
    .welcome-card {
        padding: 30px 20px;
    }
    
    .welcome-card h1 {
        font-size: 24px;
    }
    
    .exit-screen h1 {
        font-size: 32px;
        padding: 0 20px;
    }
}
</style>
""", unsafe_allow_html=True)


# ==============================
# SESSION STATE
# ==============================
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        SystemMessage(content="You are a helpful AI assistant")
    ]

if "exit" not in st.session_state:
    st.session_state.exit = False

# ==============================
# EXIT SCREEN
# ==============================
if st.session_state.exit:
    st.markdown(
        """
        <div class='exit-screen'>
            <h1>
                Thanks for chatting with
                <span class='brand'>Kronetic</span>
            </h1>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

# ==============================
# TOP NAVIGATION
# ==============================
st.markdown("""
<div class='top-nav'>
    <div class='nav-content'>
        <div class='logo-circle'>🤖</div>
        <div class='nav-title'>Kronetic</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ==============================
# EXIT BUTTON
# ==============================
st.markdown("<div class='exit-button'>", unsafe_allow_html=True)
if st.button("Exit"):
    st.session_state.exit = True
    st.rerun()
st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# CHAT SECTION
# ==============================
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Welcome message if no conversation
if len(st.session_state.chat_history) == 1:
    st.markdown("""
    <div class='welcome-card'>
        <h1>👋 Welcome to Kronetic</h1>
        <p>Your intelligent AI assistant. How can I help you today?</p>
    </div>
    """, unsafe_allow_html=True)

# Display chat messages
for msg in st.session_state.chat_history:
    if isinstance(msg, HumanMessage):
        st.chat_message("user").markdown(msg.content)
    elif isinstance(msg, AIMessage):
        st.chat_message("assistant").markdown(msg.content)

st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# USER INPUT
# ==============================
user_input = st.chat_input("Message Kronetic...")

if user_input:
    st.session_state.chat_history.append(HumanMessage(content=user_input))
    with st.spinner("Thinking..."):
        result = llm.invoke(st.session_state.chat_history)
    st.session_state.chat_history.append(AIMessage(content=result.content))
    st.rerun()

# ==============================
# FOOTER
# ==============================
st.markdown(
    "<div class='footer'>Made with ❤️ by Krish</div>",
    unsafe_allow_html=True
)