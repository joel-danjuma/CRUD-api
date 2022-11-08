from fastapi import FastAPI, Response, status, HTTPException, Depends
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .routers import post, user
from typing import List
# from dotenv import load_dotenv
# from psycopg2.extras import RealDictCursor
# import psycopg2
# import time
# import os

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# load_dotenv()
# HOST = os.getenv("HOST")
# DATABASE = os.getenv("DATABASE")
# USERNAME = os.getenv("USERNAME")
# PASSWORD = os.getenv("PASSWORD")

# while True:
#     try:
#         conn = psycopg2.connect(host=HOST, database=DATABASE, user=USERNAME, 
#         password=PASSWORD, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was succesful')
#         break
#     except Exception as error:
#         print('Connection to database failed')
#         print("Error :", error)
#         time.sleep(3)

app.include_router(post.router)
app.include_router(user.router)
#Root page for the api
@app.get("/")
def root():
    return {"message": "Welcome to my API"}

