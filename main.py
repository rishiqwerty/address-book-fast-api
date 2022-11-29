from fastapi import FastAPI, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from haversine import haversine

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
    address: str = Field(min_length=3)
    latitude: int = Field(lt=90, gt=-90)
    longitude: int = Field(lt=180, gt=-180)


# users should get addresses within given distance and cordinates
# Searched cordinates value
# Distance

'''
This is for searching the address based on latitude, longitude and
distance entered by user.
'''


@app.get('/get-address')
async def search_address(search_latitude: float, search_longitude: float, distance_in_kms: float, db: Session = Depends(get_db)):
    input_cord = (search_latitude, search_longitude)
    address_list = []
    address_model = db.query(models.Address).all()
    if address_model:
        for i in address_model:
            add_cor = (i.latitude, i.longitude)
            # if the input cordinates and the cordinates in of address in db is withing the distance input by user
            if haversine(input_cord, add_cor) <= distance_in_kms:
                address_list.append(i)
        if address_list:
            return address_list
        else:
            print(
                f'No data found input cordinates was --> {input_cord}, distance --> {distance_in_kms}')
            return 'No data found'
    else:
        return 'No data in db'

'''
This is for adding new address data
'''


@app.post('/create')
async def create_address(address: Address, db: Session = Depends(get_db)):
    address_model = models.Address()
    address_model.user = address.user
    address_model.address = address.address
    address_model.latitude = address.latitude
    address_model.longitude = address.longitude
    db.add(address_model)
    db.commit()
    return address

'''
This is for updating the address data based on address_id
'''


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
        return f'Updated!! New data: {address}'
    else:
        return f'Address id not present in DB'

'''
This is for deleting the data based on address ids
'''


@app.delete('/{address_id}')
async def delete_address(address_id: int, db: Session = Depends(get_db)):
    address_model = db.query(models.Address).filter(
        models.Address.id == address_id).first()
    if address_model:
        db.query(models.Address).filter(
            models.Address.id == address_id).delete()
        db.commit()
        return f'id: {address_id} deleted'

    else:
        return f'id: {address_id} not present'


'''
This is for getting data of all the addresses
'''


@app.get('/')
async def all_address(db: Session = Depends(get_db)):
    return db.query(models.Address).all()
