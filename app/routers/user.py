from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models, schemas, crud
from typing import List

router = APIRouter()

#get all users
@router.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM users""")
    # users = cursor.fetchall()
    users = crud.get_users(db)
    return users

#get one user by id
@router.get("/users/{id}", response_model=schemas.User)
def get_users_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM users WHERE id = %s """, (str(id)))
    # user = cursor.fetchone()
    user = crud.get_users_by_id(id,db)
    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"user with id: {id} was not found.")
    return user.first()

#get a users email by id
@router.get("/users/email/{id}")
def get_users_email_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM users WHERE id = %s """, (str(id)))
    # user = cursor.fetchone()
    user = crud.get_users_by_id(id, db)
    if not user.first():
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"user with id: {id} was not found.")
    return user.first().email

#create a new user
@router.post("/users", status_code = status.HTTP_201_CREATED, response_model=schemas.User)
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

#delete a user by its id
@router.delete("/users/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_user_by_id(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM users WHERE id = %s RETURNING * """, (str(id)))
    # deleted_user = cursor.fetchone()
    # conn.commit()
    user = crud.get_users_by_id(id, db)
    if user.first() == None :
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} does not exist.")
    user.delete(synchronize_session=False)
    db.commit()

#update users email by its id
@router.put("/users/email/{id}", response_model=schemas.User)
def update_users_email_by_id(id: int, user: schemas.UpdateUserEmail, db: Session = Depends(get_db)):
    user_query = crud.get_users_by_id(id, db)
    if user_query.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} not found")
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    return user_query.first()

#update users password by its id
@router.put("/users/password/{id}", response_model=schemas.User)
def update_users_password_by_id(id: int, user: schemas.UpdateUserPassword, db: Session = Depends(get_db)):
    user_query = crud.get_users_by_id(id, db)
    if user_query.first() == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail= f"User with id: {id} not found")
    user_query.update(user.dict(), synchronize_session=False)
    db.commit()
    # print("New user password is: " + user_query.first().password) for testing purposes, never reaveal user password!!
    return user_query.first()