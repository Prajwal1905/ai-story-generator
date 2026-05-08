from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from backend.config import OPENAI_API_KEY
import os
import re

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def score_scripts(scripts: list[str], topic: str, genre: str) -> list[float]:
    """AI scores each script variation on engagement potential"""
    llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=200)
    scores = []

    for i, script in enumerate(scripts):
        prompt = ChatPromptTemplate.from_template("""
You are a content analyst for an Indian audio drama platform.

Score this microdrama script from 0-10 based on:
- Emotional impact (3 points)
- Dialogue naturalness (2 points)
- Audio suitability (2 points)
- Cultural relevance for India (2 points)
- Strong ending (1 point)

Topic: {topic}
Genre: {genre}

Script:
{script}

Respond with ONLY a number between 0-10. Example: 7.5
""")
        chain = prompt | llm
        result = chain.invoke({
            "topic": topic,
            "genre": genre,
            "script": script
        })

        try:
            score = float(re.search(r'\d+\.?\d*', result.content).group())
            scores.append(min(score, 10.0))
        except:
            scores.append(5.0)

    return scores