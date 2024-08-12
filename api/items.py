from fastapi import APIRouter,status,HTTPException,Depends
from fastapi.responses import JSONResponse
from models import schemas,sqlmodels
from sqlalchemy.orm import Session
from typing import List
from database.db_config import connect
from repository.items import get_item,get_items,create_item
from models import sqlmodels,schemas 
from security.secure import get_current_user
items_router=APIRouter()


@items_router.post('/new/item/{owner_id}',status_code=201)
def create_new_items(req:schemas.ItemCreate,owner_id:int,current_user:sqlmodels.User=Depends(get_current_user),db:Session=Depends(connect)):
    return create_item(req=req,owner_id=owner_id,db=db)

@items_router.get('/all/items',response_model=List[schemas.ItemList])
def get_all_items(current_user:sqlmodels.User=Depends(get_current_user)
                  ,db:Session=Depends(connect)):
    return get_items(db=db)

@items_router.get('/item/{id}')
def get_item_one(id:int,current_user:sqlmodels.User=Depends(get_current_user),db:Session=Depends(connect)):
    return get_item(id=id,db=db)