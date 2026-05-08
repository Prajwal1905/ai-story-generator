from langchain_community.tools.tavily_search import TavilySearchResults
from backend.config import TAVILY_API_KEY
import os

os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY

def research_topic(topic: str) -> str:
    """Research a topic using Tavily search"""
    try:
        tool = TavilySearchResults(max_results=3)
        results = tool.invoke(topic)
        
        research_text = f"Research findings for topic: {topic}\n\n"
        for i, result in enumerate(results, 1):
            research_text += f"{i}. {result['content'][:300]}\n\n"
        
        return research_text
    except Exception as e:
        return f"Research on topic: {topic}. A story about human emotions and relationships."