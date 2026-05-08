from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from backend.config import DATABASE_URL
from backend.db.crud import save_story, get_all_stories, get_story_by_id
from backend.agent.researcher import research_topic
from backend.agent.generator import generate_script

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class StoryRequest(BaseModel):
    topic: str
    genre: str = "drama"

@router.post("/generate-story")
async def generate_story(request: StoryRequest, db: Session = Depends(get_db)):
    try:
        research = research_topic(request.topic)
        script = generate_script(
            topic=request.topic,
            genre=request.genre,
            research=research
        )
        story = save_story(
            db=db,
            topic=request.topic,
            genre=request.genre,
            script=script
        )
        return {
            "id": story.id,
            "topic": story.topic,
            "genre": story.genre,
            "script": story.script,
            "created_at": story.created_at
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/stories")
def get_stories(db: Session = Depends(get_db)):
    stories = get_all_stories(db)
    return stories

@router.get("/stories/{story_id}")
def get_story(story_id: int, db: Session = Depends(get_db)):
    story = get_story_by_id(db, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story