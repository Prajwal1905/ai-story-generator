from typing import TypedDict, List

class StoryState(TypedDict):
    topic: str
    genre: str
    research: str
    similar_stories: str
    script: str
    feedback: str
    final_script: str
    iteration: int

class PipelineState(TypedDict):
    trending_topics: List[str]
    selected_topic: str
    genre: str
    research: str
    similar_stories: str
    script_variations: List[str]
    scores: List[float]
    best_script: str
    translated_script: str
    feedback: str
    iteration: int