from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,ForeignKey,Integer,String
from sqlalchemy.orm import relationship 
Base=declarative_base()

class User(Base):
    __tablename__='user'
    id=Column('id',Integer,primary_key=True)
    username=Column('username',String,unique=True)
    password=Column('password',String)
    items=relationship('Item',back_populates='user')

class Item(Base):
    __tablename__='item'
    id=Column('id',Integer,primary_key=True)
    title=Column('title',String)
    description=Column('description',String)
    owner_id=Column('owner_id',Integer,ForeignKey('user.id'))
    user=relationship('User',back_populates='items')
    