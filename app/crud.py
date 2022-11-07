from . import models, schemas
from sqlalchemy.orm import Session

def get_posts(db: Session):
    return db.query(models.Post).all()

def get_users(db:Session):
    return db.query(models.User).all()
    
def get_post_by_id(id:int, db:Session):
    return db.query(models.Post).filter(models.Post.id == id)
    
def get_users_by_email(email:str, db:Session):
    return db.query(models.User).filter(models.User.email == email).first()

def get_users_by_id(id:int, db:Session):
    return db.query(models.User).filter(models.User.id == id)
    
def create_post(post: schemas.CreatePost, db: Session):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

def create_user(user: schemas.CreateUser, db: Session):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

