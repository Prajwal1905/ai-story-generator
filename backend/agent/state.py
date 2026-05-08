from typing import TypedDict

class StoryState(TypedDict):
    topic: str
    genre: str
    research: str
    similar_stories: str
    script: str
    feedback: str
    final_script: str
    iteration: int