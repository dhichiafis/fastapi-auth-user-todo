from sqlalchemy.orm import Session 
from models import sqlmodels,schemas


def create_item(req:schemas.ItemCreate,owner_id:int,db:Session):
    item=sqlmodels.Item(**req.dict(),owner_id=owner_id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item 

def get_items(db:Session):
    return db.query(sqlmodels.Item).all()

def get_item(id:int,db:Session):
    return db.query(sqlmodels.Item).filter(sqlmodels.Item.id==id).first()