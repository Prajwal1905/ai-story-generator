from sqlalchemy.orm import Session
from backend.db.models import Story

def save_story(db: Session, topic: str, genre: str, script: str):
    story = Story(topic=topic, genre=genre, script=script)
    db.add(story)
    db.commit()
    db.refresh(story)
    return story

def get_all_stories(db: Session):
    return db.query(Story).order_by(Story.created_at.desc()).all()

def get_story_by_id(db: Session, story_id: int):
    return db.query(Story).filter(Story.id == story_id).first()