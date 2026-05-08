from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from backend.db.models import Base
from backend.config import DATABASE_URL, APP_HOST, APP_PORT
from backend.routes.story import router as story_router
import uvicorn

app = FastAPI(title="AI Story Generator")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine = create_engine(DATABASE_URL)
Base.metadata.create_all(bind=engine)

app.include_router(story_router, prefix="/api")

@app.get("/")
def root():
    return {"message": "AI Story Generator is running!"}

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host=APP_HOST, port=APP_PORT, reload=True)