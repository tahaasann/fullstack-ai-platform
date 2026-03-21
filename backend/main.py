from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from database import engine, Base, SessionLocal, run_migrations
from routers import lessons, quizzes, progress, challenges, projects, english, goals, bookmarks, search, career
from services.content_indexer import index_content
from services.vocabulary_seeder import seed_all_english
from config import settings
from utils.logger import get_logger

logger = get_logger(__name__)

# Create all tables + run migrations for existing DB
Base.metadata.create_all(bind=engine)
run_migrations()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: index content from curriculum.json
    db = SessionLocal()
    try:
        index_content(db)
        seed_all_english(db)
    finally:
        db.close()
    yield


app = FastAPI(
    title="AI-Capable Full Stack Developer Egitim Platformu",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "detail": str(exc)}
    )


# Register routers
app.include_router(lessons.router, prefix="/api", tags=["lessons"])
app.include_router(quizzes.router, prefix="/api", tags=["quizzes"])
app.include_router(progress.router, prefix="/api", tags=["progress"])
app.include_router(challenges.router, prefix="/api", tags=["challenges"])
app.include_router(projects.router, prefix="/api", tags=["projects"])
app.include_router(english.router, prefix="/api", tags=["english"])
app.include_router(goals.router, prefix="/api", tags=["goals"])
app.include_router(bookmarks.router, prefix="/api", tags=["bookmarks"])
app.include_router(search.router, prefix="/api", tags=["search"])
app.include_router(career.router, prefix="/api", tags=["career"])


@app.get("/api/health")
def health_check() -> dict:
    return {"status": "ok", "message": "Egitim platformu calisiyor!"}
