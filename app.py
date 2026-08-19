"""
Streamlit ChatGPT-Style Agent UI with Live Thought Streaming
------------------------------------------------------------
- Pure White Light Theme (enforced by .streamlit/config.toml)
- Live Agent Thoughts rendering via StreamlitCallbackHandler
- ChatGPT-style Chat UI using native st.chat_message
"""

import os
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(
    page_title="Neonai",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Clean ChatGPT-style CSS ---
st.markdown("""
<style>
    /* Global Font & Spacing */
    .stApp {
        font-family: Söhne, ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, sans-serif !important;
    }
    
    /* Center the chat in wide mode */
    .block-container {
        max-width: 850px !important;
        padding-top: 3rem !important;
        padding-bottom: 5rem !important;
    }

    /* Remove Streamlit default header */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* Style Assistant Messages */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-assistant"]) {
        background-color: #ffffff;
        border: none;
        padding: 1rem 0;
    }
    
    /* Style User Messages */
    div[data-testid="stChatMessage"]:has(div[data-testid="chatAvatarIcon-user"]) {
        background-color: #f9f9f9;
        border-radius: 12px;
        padding: 1rem 1.5rem;
        margin-bottom: 1rem;
    }

    /* Chat Input Styling */
    div[data-testid="stChatInput"] {
        border-radius: 20px !important;
        border: 1px solid #e5e5e5 !important;
        box-shadow: 0 0 15px rgba(0,0,0,0.05) !important;
    }
</style>
""", unsafe_allow_html=True)

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_community.callbacks.streamlit import StreamlitCallbackHandler

from tools.weatherAPI import get_weather
from tools.tavilySearch import search_web
from tools.gemini import gemini_llm, ask_gemini

# --- Sidebar ---
with st.sidebar:
    st.markdown("### ⚙️ Neonai Settings")
    
    google_key = os.getenv("GOOGLE_API_KEY")
    is_key_active = google_key and "your_" not in google_key
    
    if is_key_active:
        st.success("✅ Gemini API Connected")
    else:
        st.error("⚠️ Gemini API Key Missing")

    st.markdown("---")
    st.markdown("#### Tools Available")
    use_weather = st.checkbox("⛅ Weather API", value=True)
    use_tavily = st.checkbox("🔍 Web Search", value=True)
    
    active_tools = []
    if use_weather: active_tools.append(get_weather)
    if use_tavily: active_tools.append(search_web)
    active_tools.append(ask_gemini)

    st.markdown("---")
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

# --- Agent Setup ---
template = """You are a helpful assistant. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought:{agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

agent_executor = None
if gemini_llm and is_key_active:
    try:
        agent = create_react_agent(llm=gemini_llm, tools=active_tools, prompt=prompt)
        agent_executor = AgentExecutor(
            agent=agent,
            tools=active_tools,
            verbose=True,
            handle_parsing_errors=True
        )
    except Exception:
        agent_executor = None

# --- Main App ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello, I'm Neonai! How can I help you today?"}
    ]

# Render Chat History
for message in st.session_state.messages:
    avatar = "✨" if message["role"] == "assistant" else "👤"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])

# Chat Input Field
user_query = st.chat_input("Message Neonai...")

if user_query:
    st.session_state.messages.append({"role": "user", "content": user_query})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_query)

    # Assistant Response with LIVE Agent Thoughts Streaming!
    with st.chat_message("assistant", avatar="✨"):
        if agent_executor:
            # Create the StreamlitCallbackHandler to show live "Thinking" process
            st_callback = StreamlitCallbackHandler(st.container(), expand_new_thoughts=True)
            
            try:
                # Invoke the agent with the callback handler
                res = agent_executor.invoke(
                    {"input": user_query},
                    {"callbacks": [st_callback]}
                )
                output_text = res.get("output", "Completed processing.")
            except Exception as e:
                output_text = f"**API Error**: {str(e)}\n\n*Running Weather tool fallback...*\n{get_weather.invoke({'city': user_query})}"
        else:
            output_text = "**Google API Key missing** in `.env`."
            if "weather" in user_query.lower():
                output_text += f"\n\n*Weather Fallback Result:*\n{get_weather.invoke({'city': user_query})}"

        st.markdown(output_text)
        st.session_state.messages.append({"role": "assistant", "content": output_text})
