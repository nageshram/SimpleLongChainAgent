"""
LangChain Weather API Tool
--------------------------
This module demonstrates how to create a custom Weather Tool in LangChain.
Step-by-step comments are included so you can easily follow along and learn!
"""

# STEP 1: Import required libraries
import os
import json
import urllib.request
import urllib.parse
from dotenv import load_dotenv
from langchain_core.tools import tool

# STEP 2: Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass



# STEP 3: Define a helper function to fetch weather data from a free public API
def fetch_weather_from_api(city: str) -> dict:
    """Fetch current weather data using Open-Meteo Geocoding & Weather APIs (No API key needed!)."""
    # 1. Geocode city name to latitude and longitude
    geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1&language=en&format=json"
    req = urllib.request.Request(geo_url, headers={'User-Agent': 'SimpleChatAgent/1.0'})
    
    with urllib.request.urlopen(req) as response:
        geo_data = json.loads(response.read().decode('utf-8'))
        
    if not geo_data.get("results"):
        return {"error": f"City '{city}' not found."}
        
    location = geo_data["results"][0]
    lat = location["latitude"]
    lon = location["longitude"]
    city_name = location.get("name", city)
    country = location.get("country", "")

    # 2. Fetch current weather for latitude & longitude
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
    req_weather = urllib.request.Request(weather_url, headers={'User-Agent': 'SimpleChatAgent/1.0'})
    
    with urllib.request.urlopen(req_weather) as response:
        weather_data = json.loads(response.read().decode('utf-8'))
        
    current = weather_data.get("current_weather", {})
    temperature_c = current.get("temperature")
    windspeed = current.get("windspeed")
    
    return {
        "city": f"{city_name}, {country}",
        "temperature_c": temperature_c,
        "windspeed_kmh": windspeed,
    }


# STEP 4: Create the LangChain Weather Tool using the @tool decorator
# The docstring below is critical: LangChain agents read this description to know when and how to use the tool!
@tool
def get_weather(city: str) -> str:
    """Get the current weather forecast for a given city.

    Args:
        city (str): The name of the city (e.g. 'London', 'Tokyo', 'New York').

    Returns:
        str: A human-readable summary of the current weather in that city.
    """
    try:
        data = fetch_weather_from_api(city)
        if "error" in data:
            return data["error"]
            
        city_full = data["city"]
        temp = data["temperature_c"]
        wind = data["windspeed_kmh"]
        
        return f"Current weather in {city_full}: {temp}°C with wind speed of {wind} km/h."
    except Exception as e:
        return f"Error fetching weather for '{city}': {str(e)}"


# STEP 5: Runnable code for testing the tool directly
if __name__ == "__main__":
    print("--- LangChain Weather API Tool Demo ---")
    
    # Check optional API Key setting
    weather_key = os.getenv("WEATHER_API_KEY")
    if weather_key and weather_key != "your_weather_api_key_here":
        print(f"[INFO] Using configured WEATHER_API_KEY: {weather_key[:4]}...")
    else:
        print("[INFO] No WEATHER_API_KEY needed; using free Open-Meteo live weather data.")

    # Test the LangChain tool with sample cities
    test_cities = ["London", "Tokyo", "New York"]
    
    for c in test_cities:
        print(f"\nQuerying weather for '{c}'...")
        # Invoke the LangChain tool via ask / invoke
        result = get_weather.invoke({"city": c})
        print(f"Tool Output: {result}")
