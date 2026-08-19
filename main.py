import os
from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate

# Pulling LLM and Tools from tools/ folder
from tools.weatherAPI import get_weather
from tools.gemini import gemini_llm, ask_gemini
from tools.tavilySearch import search_web

# Set Google Gemini as the LLM brain
selected_llm = gemini_llm

# Assemble available tools list
tools = [get_weather, search_web, ask_gemini]

# ReAct prompt template
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

# Create Agent and Executor
if selected_llm:
    agent = create_react_agent(llm=selected_llm, tools=tools, prompt=prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
else:
    agent_executor = None

if __name__ == "__main__":
    print("--- LangChain Interactive Agent (Powered by Google Gemini + Tools) ---")
    
    while True:
        user_input = input("\nEnter your question (Q or q to quit): ")
        if user_input.strip().lower() in ["q", "quit", "exit"]:
            print("Thanks for using the Gemini Chat Agent!")
            break
            
        active_key = os.getenv("GOOGLE_API_KEY")
        
        # If API key is missing, fall back to direct weather tool execution
        if not active_key or "your_" in active_key or not agent_executor:
            print("[WARNING] GOOGLE_API_KEY is not set in .env file.")
            print("Get a free Gemini API Key at: https://aistudio.google.com")
            print(f"\nDirect Weather Tool Execution for '{user_input}':")
            print(get_weather.invoke({"city": user_input}))
        else:
            try:
                response = agent_executor.invoke({"input": user_input})
                print("\nFinal Output:")
                print(response["output"])
            except Exception as e:
                err_msg = str(e)
                print(f"\n[API ERROR] Call to Gemini failed: {err_msg}")
                print(f"\nExecuting Weather tool directly for '{user_input}':")
                print(get_weather.invoke({"city": user_input}))
