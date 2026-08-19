"""
LangChain Tavily Web Search Tool
--------------------------------
This module demonstrates how to create a Tavily Web Search Tool in LangChain.
Tavily is an AI-powered search engine that allows agents to search live web information!
"""

# STEP 1: Import required libraries
import os
from dotenv import load_dotenv
load_dotenv()

from langchain_core.tools import tool

try:
    from tavily import TavilyClient
except ImportError:
    TavilyClient = None

# STEP 2: Retrieve TAVILY_API_KEY from environment variables
tavily_api_key = os.getenv("TAVILY_API_KEY")

# STEP 3: Initialize TavilyClient
if TavilyClient and tavily_api_key and "your_" not in tavily_api_key:
    tavily_client = TavilyClient(api_key=tavily_api_key)
else:
    tavily_client = None


# STEP 4: Define the LangChain Tool using @tool decorator
@tool
def search_web(query: str) -> str:
    """Search the live web using Tavily Search API for up-to-date information, news, and facts.

    Args:
        query (str): The search query or topic to search on the web.

    Returns:
        str: A formatted summary of the top search results found on the web.
    """
    if not tavily_client:
        return "Tavily Search API key is not configured in .env file. Get a free key at https://tavily.com."
    
    try:
        response = tavily_client.search(query=query, max_results=3)
        results = response.get("results", [])
        
        if not results:
            return f"No web search results found for query: '{query}'"
            
        summary = []
        for i, res in enumerate(results, 1):
            title = res.get("title", "No Title")
            content = res.get("content", "")
            url = res.get("url", "")
            summary.append(f"Result {i}:\nTitle: {title}\nSummary: {content}\nURL: {url}")
            
        return "\n\n".join(summary)
    except Exception as e:
        return f"Error executing Tavily web search: {str(e)}"


# STEP 5: Runnable code for testing the tool directly
if __name__ == "__main__":
    print("--- LangChain Tavily Web Search Demo ---")
    
    if not tavily_api_key or "your_" in tavily_api_key:
        print("[WARNING] TAVILY_API_KEY is not set or using placeholder in .env file.")
        print("Get a free Tavily Search API key at: https://tavily.com")
    elif not TavilyClient:
        print("[WARNING] tavily-python package is not installed.")
        print("Please run: pip install tavily-python")
    else:
        sample_query = "What is the latest news in AI today?"
        print(f"\nSearching web for: '{sample_query}'")
        res = search_web.invoke({"query": sample_query})
        print(f"\nSearch Results:\n{res}")
