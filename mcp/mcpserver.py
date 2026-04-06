from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()


mcp = FastMCP("weather-server")

@mcp.tool(description="Get the current weather for a city")
def get_weather(city: str) -> str:
    return f"{city}: 32°C, Clear"

@mcp.tool(description="Get the capital of a country")
def get_capital(country: str) -> str:
    
    api_key = os.getenv("TAVILY_API_KEY")
    print(api_key)
    client = TavilyClient(api_key=api_key)
    
    
    response = client.search(f"capital of {country}")
    if response["results"]:
        return response["results"][0]["content"]
    return f"{country}: Capital not found"

if __name__ == "__main__":
    mcp.run()