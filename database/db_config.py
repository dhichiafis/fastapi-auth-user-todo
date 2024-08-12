from sqlalchemy import create_engine


from sqlalchemy.orm import sessionmaker 


DATABASE='sqlite:///./usertodo.db'

engine=create_engine(DATABASE)

SessionFactory=sessionmaker(autocommit=False,autoflush=False,bind=engine)


def connect():
    db=SessionFactory()
    try:
        yield db 
        
    finally:
        db.close()