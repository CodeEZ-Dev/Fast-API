from typing import Optional, List
from fastapi import FastAPI, HTTPException, status,Response,Depends,APIRouter
from fastapi.params import Body
from sqlalchemy.orm import Session
from .. import models,schema,utils
from ..database import engine,SessionLocal,get_db

router = APIRouter(
    prefix='/users',
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schema.UserOut)
def create_user(user:schema.CreateUser,db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get("/{id}",response_model=schema.UserOut)
def get_user(id:int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return user