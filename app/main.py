from fastapi import FastAPI, Response, status, HTTPException, Depends
from .database import engine
from . import models, schemas, crud
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

#Root page for the api
@app.get("/")
def root():
    return {"message": "Welcome to my API"}

