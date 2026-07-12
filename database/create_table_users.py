from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from connectDB import Base, engine

class User(Base):
    __tablename__ = "Users"
    Id = Column(Integer, primary_key = True, index= True, autoincrement= True)
    username = Column(String(50))
    password = Column(String(255)),
    role = Column(String(20))

Base.metadata.create_all(bing = engine)
print("Table Users cree avec succes !")