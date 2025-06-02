from backend.utlis.db import Base
from sqlalchemy import Column, Integer, String

class KeywordModel(Base):
    __tablename__ = "Keyword"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(50), nullable=False, unique=True)
    action = Column(String(50), nullable=False)