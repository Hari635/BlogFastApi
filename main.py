from fastapi import FastAPI
from post import  models
from post.database import engine
from post.routers import post

app = FastAPI()

models.Base.metadata.create_all(engine)
app.include_router(post.router)