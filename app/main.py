from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# Creates all tables when app is starting up. Don't using this anymore. Instead using Alembic
# models.Base.metadata.create_all(bind=engine)


# Command to run app: uvicorn app.main:app --reload
app = FastAPI()

# public API, i.e. every single domain can access it
# in case API is created to use only by specific app, we need to specify domains, which can use it
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
