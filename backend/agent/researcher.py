from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from backend.config import TAVILY_API_KEY, OPENAI_API_KEY
import os

os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def research_topic(topic: str) -> str:
    """Research Agent — searches web and summarizes findings"""
    try:
        # Search web
        tool = TavilySearchResults(max_results=3)
        results = tool.invoke(topic)
        
        raw_research = ""
        for i, result in enumerate(results, 1):
            raw_research += f"{i}. {result['content'][:300]}\n\n"
        
        # Summarize with LLM
        llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=500)
        prompt = ChatPromptTemplate.from_template("""
You are a research assistant for a storytelling platform.

Topic: {topic}

Raw research:
{raw_research}

Summarize the key emotional themes, cultural context, and story angles 
related to this topic in 3-4 sentences. Focus on what makes compelling stories.
""")
        chain = prompt | llm
        result = chain.invoke({"topic": topic, "raw_research": raw_research})
        return result.content

    except Exception as e:
        return f"Topic '{topic}' explores deep human emotions and relationships that resonate with Indian audiences."