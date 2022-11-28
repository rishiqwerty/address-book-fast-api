from fastapi import FastAPI
from pydantic import BaseModel, Field
app = FastAPI()

class Address(BaseModel):
    id: int
    user: str = Field(min_length=1)
    address: str = Field(min_length=10)
    latitude: int = Field(Lt=1000)
    longitude: int = Field(Lt=1000)

ADDRESSES = []

@app.get('/')
async def test():
    return ADDRESSES

@app.post('/create')
async def create_address(address: Address):
    ADDRESSES.append(address)
    return address

@app.put('/{address_id}')
async def update_address(address_id: int, address: Address):

    for i in ADDRESSES:
        if address_id == i.id:
            ADDRESSES[ADDRESSES.index(i)] = address
            return ADDRESSES[ADDRESSES.index(i)]
@app.delete('/{address_id}')
async def delete_address(address_id: int):
    for x in ADDRESSES:
        if address_id == x.id:
            del ADDRESSES[ADDRESSES.index(x)]
            return f'id: {address_id} deleted'