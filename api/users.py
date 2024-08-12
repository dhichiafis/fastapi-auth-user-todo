from fastapi import APIRouter,status,HTTPException,Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from security.secure import authenticate_user,get_password_hash,create_access_token,get_current_user
from database.db_config import connect
from sqlalchemy.orm import Session
from datetime import time,timedelta,timezone
from models import schemas,sqlmodels
from typing import List
user_router=APIRouter()


@user_router.post("/token")
async def login_for_access_token(
    form_data:OAuth2PasswordRequestForm =Depends(),db:Session=Depends(connect)
) -> schemas.Token:
    user = authenticate_user(form_data.username, form_data.password,db)
    if not user:
        raise HTTPException(
            
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return schemas.Token(access_token=access_token, token_type="bearer")


@user_router.post('/new/user',status_code=201,response_model=schemas.UserList)
def create_new_user(req:schemas.UserCreate,db:Session=Depends(connect)):
    user_db=db.query(sqlmodels.User).filter(sqlmodels.User.username==req.username).first()
    if user_db:
        raise HTTPException(status=401,detail='user already exist')
    password=get_password_hash(req.password)
    user_db=sqlmodels.User(username=req.username,password=password)
    db.add(user_db)
    db.commit()
    db.refresh(user_db)
    return user_db

@user_router.get('/all/users',response_model=List[schemas.UserList])
def get_all_users(db:Session=Depends(connect),
    current_user:sqlmodels.User=Depends(get_current_user)):
    return db.query(sqlmodels.User).all()

@user_router.get('/user/{id}')
def get_user(id:int,db:Session=Depends(connect),current_user:sqlmodels.User=Depends(get_current_user)):
    return db.query(sqlmodels.User).filter(sqlmodels.User.id==id).first()



@user_router.get('/user/{owner_id}/items')
def get_user_items(owner_id:int,current_user:sqlmodels.User=Depends(get_current_user),db:Session=Depends(connect)):
    
    return db.query(sqlmodels.Item).filter(sqlmodels.Item.owner_id==owner_id).all()

@user_router.get("/user/me/", response_model=schemas.UserList)
async def read_users_me(
    current_user:sqlmodels.User=Depends(get_current_user),
):
    return current_user