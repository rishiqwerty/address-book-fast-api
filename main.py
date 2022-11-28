from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db

    finally:
        db.close()


class Address(BaseModel):
    # id: int
    user: str = Field(min_length=1)
    address: str = Field(min_length=10)
    latitude: int = Field(Lt=1000)
    longitude: int = Field(Lt=1000)


ADDRESSES = []


@app.get('/')
async def test(db: Session = Depends(get_db)):
    return db.query(models.Address).all()


@app.post('/create')
async def create_address(address: Address, db: Session = Depends(get_db)):
    address_model = models.Address()
    address_model.user = address.user
    address_model.address = address.address
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude
    # ADDRESSES.append(address)
    db.add(address_model)
    db.commit()
    return address


@app.put('/{address_id}')
async def update_address(address_id: int, address: Address, db: Session = Depends(get_db)):
    address_model = db.query(models.Address).filter(
        models.Address.id == address_id).first()
    if address_model:
        address_model.user = address.user
        address_model.address = address.address
        address_model.latitude = address.latitude
        address_model.longitude = address.longitude

        db.add(address_model)
        db.commit()
        return address


@app.delete('/{address_id}')
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    address_model = db.query(models.Address).filter(
        models.Address.id == address_id).first()
    if address_model:
        db.query(models.Address).filter(
            models.Address.id == address_id).delete()
        db.commit()
        return f'id: {address_id} deleted'
