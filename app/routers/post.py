from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, crud, oauth2
from typing import List

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

#get all posts
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    posts = crud.get_posts(db)
    return posts

#get one post by id
@router.get("/{id}", response_model=schemas.Post)
def get_posts_by_id(id: int, db: Session = Depends(get_db)):
    post = crud.get_post_by_id(id,db)
    if not post.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found.")
    return post.first()

#create a new post
@router.post('/', status_code = status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post : schemas.CreatePost, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    new_post = crud.create_post(post,db)
    return new_post

#delete a post by its id
@router.delete("/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post_by_id(id: int, db: Session= Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post = crud.get_post_by_id(id, db)
    if post.first() == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"Post with id: {id} does not exist.")
    post.delete(synchronize_session=False)
    db.commit()
    
#update posts by its id
@router.put("/{id}")
def update_posts(id: int, post : schemas.CreatePost, db: Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post_query = crud.get_post_by_id(id, db)
    if post_query.first() == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} does not exist.")
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()