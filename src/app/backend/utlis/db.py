from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:root@mysql/votary_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

class Base(DeclarativeBase): pass

def get_db():
    db = SessionLocal()
    try: 
        yield db
    finally:
        db.close()
