from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from typing import List

router = APIRouter()

#get all posts
@router.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).all()
    posts = crud.get_posts(db)
    return posts

#get one post by id
@router.get("/posts/{id}", response_model=schemas.Post)
async def get_posts_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * from posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    post = crud.get_post_by_id(id,db)
    if not post.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found.")
    return post.first()

#create a new post
@router.post('/posts', status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
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

#delete a post by its id
@router.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session= Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post = crud.get_post_by_id(id, db)
    if post.first() == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist.")
    post.delete(synchronize_session=False)
    db.commit()
    
#update posts by its id
@router.put("/posts/{id}")
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