from fastapi import FastAPI

from app.apis.base import api_router
from app.core.config import settings
from app.db.db_model import Base, engine


# Create database
def create_tables():
    Base.metadata.create_all(bind=engine)


def include_router(app):
    app.include_router(api_router)


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app


app = start_application()


@app.get("/")
async def root():
    return {"message": "Hello World"}
