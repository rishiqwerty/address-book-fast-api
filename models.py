from sqlalchemy import Column, Integer, String
from database import Base

class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    address = Column(String)
    longitude = Column(Integer)
    latitude = Column(Integer)