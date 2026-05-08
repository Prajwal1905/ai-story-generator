from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from backend.config import TAVILY_API_KEY, OPENAI_API_KEY
import os

os.environ["TAVILY_API_KEY"] = TAVILY_API_KEY
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def get_trending_topics(genre: str = "drama") -> list[str]:
    """Fetches trending topics from web relevant to Indian audio stories"""
    try:
        tool = TavilySearchResults(max_results=5)
        results = tool.invoke(
            f"trending emotional story topics India 2025 {genre} audio drama"
        )

        raw = "\n".join([r['content'][:200] for r in results])

        llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=300)
        prompt = ChatPromptTemplate.from_template("""
You are a content strategist for Kuku FM, India's leading audio platform.

Based on this trending content from the web:
{raw}

Extract exactly 5 trending story topics that would make compelling {genre} microdramas for Indian audiences.
Topics should be emotional, relatable, and culturally relevant.

Return ONLY a Python list like:
["topic1", "topic2", "topic3", "topic4", "topic5"]
""")
        chain = prompt | llm
        result = chain.invoke({"raw": raw, "genre": genre})

        import ast
        topics = ast.literal_eval(result.content.strip())
        return topics[:5]

    except Exception as e:
        return [
            "long distance relationship",
            "career vs family pressure",
            "toxic friendship",
            "startup failure",
            "identity crisis"
        ]