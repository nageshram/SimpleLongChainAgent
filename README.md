# Neonai (SimpleLongChainAgent)

A ChatGPT-style interactive chat agent powered by LangChain and Google Gemini. Neonai is equipped with multiple tools to answer questions, search the web, and provide live weather updates. It comes with both a sleek Streamlit web application and a command-line interface (CLI).

## Features

- **Google Gemini LLM Brain**: Utilizes Google's Gemini models for powerful conversational capabilities.
- **ReAct Agent Architecture**: The agent intelligently plans its thoughts and selects appropriate tools to solve complex queries.
- **Streamlit Web UI**: A clean, white-light theme ChatGPT-style web application (`app.py`) featuring live thought-process streaming.
- **CLI Mode**: A lightweight terminal-based interactive agent (`main.py`).
- **Integrated Tools**:
  - ⛅ **Weather API**: Real-time weather fetching.
  - 🔍 **Tavily Web Search**: Fast, accurate web searching for real-time information.
  - ✨ **Gemini Fallback**: Direct querying capabilities when tools aren't necessary.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/nageshram/SimpleLongChainAgent.git
   cd SimpleLongChainAgent
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   Create a `.env` file in the root directory and add your API keys:
   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   # Add any other required API keys (e.g., for the Weather tool)
   ```

## Usage

### Run the Web Interface
To launch the modern Streamlit web application:
```bash
streamlit run app.py
```

### Run the Command Line Interface
To use the agent directly from your terminal:
```bash
python main.py
```

## Technologies Used
- [LangChain](https://python.langchain.com/)
- [Streamlit](https://streamlit.io/)
- [Google Gemini](https://ai.google.dev/)
- [Tavily Search](https://tavily.com/)
