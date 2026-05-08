from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from backend.config import OPENAI_API_KEY
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

SUPPORTED_LANGUAGES = {
    "hindi": "Hindi",
    "tamil": "Tamil",
    "telugu": "Telugu",
    "kannada": "Kannada",
    "bengali": "Bengali"
}

def translate_script(script: str, language: str) -> str:
    """Translates script to Indian regional language"""
    if language not in SUPPORTED_LANGUAGES:
        return script

    llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=1500)
    prompt = ChatPromptTemplate.from_template("""
Translate this microdrama script to {language}.

Keep the same format, character names can be adapted to suit {language} culture.
Make the dialogue sound natural in {language}, not like a direct translation.

Script:
{script}

Translated script:
""")
    chain = prompt | llm
    result = chain.invoke({
        "language": SUPPORTED_LANGUAGES[language],
        "script": script
    })
    return result.content