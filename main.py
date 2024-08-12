from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware
import uvicorn 
from api import items,users
import models.sqlmodels
from database.db_config import engine
origins=['http://localhost:8000','http://localhost:5173']
models.sqlmodels.Base.metadata.create_all(bind=engine)

app=FastAPI()
app.add_middleware(CORSMiddleware,allow_origins=origins
    ,allow_headers=['*'],allow_methods=['*'],allow_credentials=True)
app.include_router(users.user_router,prefix='/users')
app.include_router(items.items_router,prefix='/items')
if __name__=="__main__":
    uvicorn.run("main:app",reload=True,host='127.0.0.1',port=8000)