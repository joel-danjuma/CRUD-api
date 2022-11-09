from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import database, schemas, crud, utils

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login")
def login(user_credentials : schemas.UserLogin, db: Session = Depends(database.get_db)):
   user = crud.get_users_by_email(user_credentials.email, db)
   if not user:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid credentials")
   if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials")
   return {"token" : "example token"} 