from fastapi import FastAPI, Response, status, HTTPException, Depends
from .database import engine, get_db
from sqlalchemy.orm import Session
from . import models, schemas, crud
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

#Root page for the api
@app.get("/")
def root():
    return {"message": "Welcome to my API"}

#get all posts
@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).all()
    posts = crud.get_posts(db)
    return posts

#get all users
@app.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM users""")
    # users = cursor.fetchall()
    users = crud.get_users(db)
    return users

#get one post by id
@app.get("/posts/{id}", response_model=schemas.Post)
async def get_posts_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = crud.get_post_by_id(id,db)
    if not post.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found.")
    return post.first()

#get one user by id
@app.get("/users/{id}", response_model=schemas.User)
def get_users_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM users WHERE id = %s """, (str(id)))
    # user = cursor.fetchone()
    user = crud.get_users_by_id(id,db)
    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"user with id: {id} was not found.")
    return user.first()

#get a users email by id
@app.get("/users/email/{id}")
def get_users_email_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM users WHERE id = %s """, (str(id)))
    # user = cursor.fetchone()
    user = crud.get_users_by_id(id, db)
    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"user with id: {id} was not found.")
    return user.first().email

#create a new post
@app.post('/posts', status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s, %s) RETURNING * """, 
    #     (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # print("created new post")
    # conn.commit()
    # db.add(new_post)
    # db.commit()
    # db.refresh(new_post)
    new_post = crud.create_post(post,db)
    return new_post

#create a new user
@app.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO users (name, age, address, school, is_graduate, is_employed) VALUES(%s, %s, %s, %s, %s, %s) RETURNING * """,
    #     (user.name, user.age, user.address, user.school, user.is_graduate, user.is_employed))
    # new_user = cursor.fetchone()
    # print("created new user")
    # conn.commit()
    # db.add(new_user)
    # db.commit()
    # db.refresh(new_user)
    db_user = crud.get_users_by_email(user.email, db)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The user already exists")
    new_user = crud.create_user(user,db)
    return new_user

#delete a post by its id
@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session= Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = crud.get_post_by_id(id, db)
    if post.first() == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist.")
    post.delete(synchronize_session=False)
    db.commit()
    
#delete a user by its id
@app.delete("/users/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM users WHERE id = %s RETURNING * """, (str(id)))
    # deleted_user = cursor.fetchone()
    # conn.commit()
    user = crud.get_users_by_id(id, db)
    if user.first() == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} does not exist.")
    user.delete(synchronize_session=False)
    db.commit()
    
#update posts by its id
@app.put("/posts/{id}")
def update_posts(id: int, post : schemas.CreatePost, db: Session = Depends(get_db)):
    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = crud.get_post_by_id(id, db)
    if post_query.first() == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist.")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()

#update users email by its id
@app.put("/users/email/{id}", response_model=schemas.User)
def update_users_email_by_id(id: int, user: schemas.UpdateUserEmail, db: Session = Depends(get_db)):
    user_query = crud.get_users_by_id(id, db)
    if user_query.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} not found")
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()

#update users password by its id
@app.put("/users/password/{id}", response_model=schemas.User)
def update_users_password_by_id(id: int, user: schemas.UpdateUserPassword, db: Session = Depends(get_db)):
    user_query = crud.get_users_by_id(id, db)
    if user_query.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} not found")
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    # print("New user password is: " + user_query.first().password) for testing purposes, never reaveal user password!!
    return user_query.first()