from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from backend.config import ANTHROPIC_API_KEY
from backend.rag.retriever import retrieve_similar_stories
import os

os.environ["ANTHROPIC_API_KEY"] = ANTHROPIC_API_KEY

# Define agent state
class StoryState(TypedDict):
    topic: str
    genre: str
    research: str
    similar_stories: str
    script: str
    feedback: str
    iteration: int

# Initialize LLM
llm = ChatAnthropic(model="claude-3-haiku-20240307", max_tokens=1500)

# Node 1 — RAG retrieval
def rag_node(state: StoryState) -> StoryState:
    similar = retrieve_similar_stories(state["topic"])
    state["similar_stories"] = similar
    return state

# Node 2 — Generate script
def generate_node(state: StoryState) -> StoryState:
    prompt = ChatPromptTemplate.from_template("""
You are a microdrama script writer for an Indian audio platform like Kuku FM.

Topic: {topic}
Genre: {genre}

Research Context:
{research}

Similar Story Examples:
{similar_stories}

Write a short microdrama script with:
- 2-3 characters with Indian names
- 3 scenes maximum
- Emotional and engaging dialogue
- Each scene max 4-5 lines
- End with a strong emotional punch

Format:
TITLE: [title]

CHARACTERS:
- [character 1]
- [character 2]

SCENE 1:
[dialogue]

SCENE 2:
[dialogue]

SCENE 3:
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

# Node 3 — Reflection (ReAct pattern)
def reflect_node(state: StoryState) -> StoryState:
    prompt = ChatPromptTemplate.from_template("""
You are a script quality reviewer.

Review this microdrama script and check:
1. Is it emotional and engaging?
2. Does it suit the topic: {topic}?
3. Is the dialogue natural?

Script:
{script}

If the script is good respond with: APPROVED
If it needs improvement respond with: IMPROVE: [specific feedback]
""")
    
    chain = prompt | llm
    result = chain.invoke({
        "topic": state["topic"],
        "script": state["script"]
    })
    state["feedback"] = result.content
    state["iteration"] = state.get("iteration", 0) + 1
    return state

# Node 4 — Improve script if needed
def improve_node(state: StoryState) -> StoryState:
    prompt = ChatPromptTemplate.from_template("""
Improve this microdrama script based on the feedback.

Original script:
{script}

Feedback:
{feedback}

Write an improved version keeping the same format.
""")
    
    chain = prompt | llm
    result = chain.invoke({
        "script": state["script"],
        "feedback": state["feedback"]
    })
    state["script"] = result.content
    return state

# Conditional edge — should we improve or finish?
def should_improve(state: StoryState) -> str:
    if state["iteration"] >= 2:
        return "end"
    if "APPROVED" in state["feedback"]:
        return "end"
    return "improve"

# Build LangGraph
def build_graph():
    graph = StateGraph(StoryState)
    
    graph.add_node("rag", rag_node)
    graph.add_node("generate", generate_node)
    graph.add_node("reflect", reflect_node)
    graph.add_node("improve", improve_node)
    
    graph.set_entry_point("rag")
    graph.add_edge("rag", "generate")
    graph.add_edge("generate", "reflect")
    graph.add_conditional_edges("reflect", should_improve, {
        "improve": "improve",
        "end": END
    })
    graph.add_edge("improve", END)
    
    return graph.compile()

# Main function called from routes
def generate_script(topic: str, genre: str, research: str) -> str:
    graph = build_graph()
    result = graph.invoke({
        "topic": topic,
        "genre": genre,
        "research": research,
        "similar_stories": "",
        "script": "",
        "feedback": "",
        "iteration": 0
    })
    return result["script"]