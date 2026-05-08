from typing import Any
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from backend.config import OPENAI_API_KEY
from backend.rag.retriever import retrieve_similar_stories
from backend.agent.researcher import research_topic
import os

os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY



def research_agent(state: StoryState) -> StoryState:
    """Researches the topic using Tavily + LLM summarization"""
    print(" Research Agent working...")
    research = research_topic(state["topic"])
    state["research"] = research
    return state

def rag_agent(state: StoryState) -> StoryState:
    """Retrieves similar stories from ChromaDB vector store"""
    print(" RAG Agent working...")
    similar = retrieve_similar_stories(state["topic"])
    state["similar_stories"] = similar
    return state

def writer_agent(state: StoryState) -> StoryState:
    """Writes the microdrama script based on research and similar stories"""
    print(" Writer Agent working...")
    llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=1500)
    prompt = ChatPromptTemplate.from_template("""
You are an expert microdrama script writer for Kuku FM, India's leading audio platform.

Topic: {topic}
Genre: {genre}

Research Insights:
{research}

Similar Story Examples for reference:
{similar_stories}

Write an emotionally powerful microdrama script with:
- 2-3 characters with authentic Indian names
- Exactly 3 scenes
- Natural conversational dialogue
- Strong emotional hook in Scene 1
- Conflict or revelation in Scene 2
- Powerful emotional punch in Scene 3
- Each scene: 4-5 lines of dialogue only

Format strictly as:
TITLE: [compelling title]

CHARACTERS:
- [Name]: [one line description]
- [Name]: [one line description]

SCENE 1: [scene title]
[dialogue]

SCENE 2: [scene title]
[dialogue]

SCENE 3: [scene title]
[dialogue]
""")
    chain = prompt | llm
    result = chain.invoke({
        "topic": state["topic"],
        "genre": state["genre"],
        "research": state["research"],
        "similar_stories": state["similar_stories"]
    })
    state["script"] = result.content
    return state

def critic_agent(state: StoryState) -> StoryState:
    """Reviews the script and provides specific feedback (ReAct pattern)"""
    print(" Critic Agent reviewing...")
    llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=600)
    prompt = ChatPromptTemplate.from_template("""
You are a senior script editor for an Indian audio drama platform.

Review this microdrama script critically:

Topic: {topic}
Genre: {genre}

Script:
{script}

Evaluate on:
1. Emotional impact (does it make you feel something?)
2. Authenticity (does it feel real and Indian?)
3. Dialogue quality (natural or forced?)
4. Story structure (clear beginning, conflict, resolution?)
5. Audio suitability (works without visuals?)

Respond with ONLY one of these:
- APPROVED: [one line reason]
- IMPROVE: [specific actionable feedback in 2-3 sentences]
""")
    chain = prompt | llm
    result = chain.invoke({
        "topic": state["topic"],
        "genre": state["genre"],
        "script": state["script"]
    })
    state["feedback"] = result.content
    state["iteration"] = state.get("iteration", 0) + 1
    return state

def rewriter_agent(state: StoryState) -> StoryState:
    """Rewrites the script based on critic feedback"""
    print(" Rewriter Agent improving...")
    llm = ChatOpenAI(model="gpt-3.5-turbo", max_tokens=1500)
    prompt = ChatPromptTemplate.from_template("""
You are a script rewriter for an Indian audio drama platform.

Original script:
{script}

Editor feedback:
{feedback}

Rewrite the script addressing ALL the feedback points.
Keep the same format, same characters, but improve the dialogue and structure.
Make it more emotional, authentic, and powerful.
""")
    chain = prompt | llm
    result = chain.invoke({
        "script": state["script"],
        "feedback": state["feedback"]
    })
    state["script"] = result.content
    return state

def finalizer_agent(state: StoryState) -> StoryState:
    """Finalizes and polishes the script"""
    print(" Finalizer Agent polishing...")
    state["final_script"] = state["script"]
    return state

def should_rewrite(state: StoryState) -> str:
    if state["iteration"] >= 2:
        return "finalize"
    if state["feedback"].startswith("APPROVED"):
        return "finalize"
    return "rewrite"

def build_multi_agent_graph():
    graph = StateGraph(StoryState)

    # Add all agents as nodes
    graph.add_node("research", research_agent)
    graph.add_node("rag", rag_agent)
    graph.add_node("writer", writer_agent)
    graph.add_node("critic", critic_agent)
    graph.add_node("rewriter", rewriter_agent)
    graph.add_node("finalizer", finalizer_agent)

    # Define flow
    graph.set_entry_point("research")
    graph.add_edge("research", "rag")
    graph.add_edge("rag", "writer")
    graph.add_edge("writer", "critic")
    graph.add_conditional_edges("critic", should_rewrite, {
        "rewrite": "rewriter",
        "finalize": "finalizer"
    })
    graph.add_edge("rewriter", "critic")
    graph.add_edge("finalizer", END)

    return graph.compile()


def run_multi_agent(topic: str, genre: str) -> str:
    graph = build_multi_agent_graph()
    result = graph.invoke({
        "topic": topic,
        "genre": genre,
        "research": "",
        "similar_stories": "",
        "script": "",
        "feedback": "",
        "final_script": "",
        "iteration": 0
    })
    return result["final_script"]