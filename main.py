from fastapi import FastAPI
from pydantic import BaseModel, Field
app = FastAPI()

a = {
    'Name': 'Unknown',
    'Address': 'Mango',
    'Latitude': 23,
    'Longitude': 32
}

class Address(BaseModel):
    id: int
    user: str = Field(min_length=1)
    address: str = Field(min_length=10)
    latitude: int
    longitude: int

ADDRESSES = []

@app.get('/')
async def test():
    return ADDRESSES

@app.post('/create')
async def create_address(address: Address):
    ADDRESSES.append(address)
    return address