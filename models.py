from sqlalchemy import Column, Integer, String, Float
from database import Base


class Address(Base):
    __tablename__ = "address"

    id = Column(Integer, primary_key=True, index=True)
    user = Column(String)
    address = Column(String)
    longitude = Column(Float)
    latitude = Column(Float)
