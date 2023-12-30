from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from pydantic import BaseModel
from bson.objectid import ObjectId
from enum import Enum
from typing import Union, List

app = FastAPI()

# MongoDB connection URL
# MONGO_URL = "mongodb://my-mongodb:27017"
MONGO_URL ="mongodb://localhost:27017"
client = MongoClient(MONGO_URL)
db = client["car_platform"]
cars_collection = db["cars"]
brokers_collection = db["brokers"]

# Data Models
class CarStatus(str, Enum):
    INACTIVE = "inactive"
    ACTIVE = "active"
    SOLD = "sold"

class Car(BaseModel):
    brand: str
    model: str
    year: int
    color: str
    mileage: float
    status: CarStatus

class Broker(BaseModel):
    name: str
    branches: str
    mobile: str
    email: str

class Listing(BaseModel):
    status: CarStatus

@app.get("/")
async def root():
    return {"message": "Hello World"}

# API Endpoints

@app.post("/cars/")
async def create_car(cars: Union[Car, List[Car]]):
    try:
        if isinstance(cars, list):
            # If it's a list, insert each car individually
            inserted_ids = [cars_collection.insert_one(car.model_dump()).inserted_id for car in cars]
            return JSONResponse(content={"car_ids": [str(car_id) for car_id in inserted_ids]}, status_code=201)
        else:
            # If it's a single car, insert it
            car_data = cars.model_dump()
            car_id = cars_collection.insert_one(car_data).inserted_id
            return JSONResponse(content={"car_id": str(car_id)}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cars/{car_id}", response_model=Car)
async def read_car(car_id: str):
    try:
        car = cars_collection.find_one({"_id": ObjectId(car_id)})
        if car is not None:
            return car
        else:
            raise HTTPException(status_code=404, detail="Car not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/cars/{car_id}")
async def update_car(car_id: str, car: Car):
    try:
        updated_car = cars_collection.update_one(
            {"_id": ObjectId(car_id)}, {"$set": car.model_dump()}
        )
        if updated_car.modified_count == 1:
            return {"message": "Car updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Car not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/cars/{car_id}")
async def delete_car(car_id: str):
    try:
        deleted_car = cars_collection.delete_one({"_id": ObjectId(car_id)})
        if deleted_car.deleted_count == 1:
            return {"message": "Car deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Car not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/cars/{car_id}/status", response_model=Listing)
async def get_car_status(car_id: str):
    try:
        car = cars_collection.find_one({"_id": ObjectId(car_id)})
        if car is not None:
            return {"status": car["status"]}
        else:
            raise HTTPException(status_code=404, detail="Car not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# For Brokers
@app.post("/brokers/")
async def create_broker(broker: Broker):
    try:
        broker_data = broker.model_dump()
        broker_id = brokers_collection.insert_one(broker_data).inserted_id
        return JSONResponse(content={"broker_id": str(broker_id)}, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/brokers/{broker_id}", response_model=Broker)
async def read_broker(broker_id: str):
    try:
        broker = brokers_collection.find_one({"_id": ObjectId(broker_id)})
        if broker is not None:
            return broker
        else:
            raise HTTPException(status_code=404, detail="Broker not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/brokers/{broker_id}")
async def update_broker(broker_id: str, broker: Broker):
    try:
        updated_broker = brokers_collection.update_one(
            {"_id": ObjectId(broker_id)}, {"$set": broker.model_dump()}
        )
        if updated_broker.modified_count == 1:
            return {"message": "Broker updated successfully"}
        else:
            raise HTTPException(status_code=404, detail="Broker not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/brokers/{broker_id}")
async def delete_broker(broker_id: str):
    try:
        deleted_broker = brokers_collection.delete_one({"_id": ObjectId(broker_id)})
        if deleted_broker.deleted_count == 1:
            return {"message": "Broker deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Broker not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/listing/cars/", response_model=list[Car])
async def get_model(
    brand: str = None,
    model: str = None,
    year: int = None,
    color: str = None,
    mileage: float = None,
    status: CarStatus = None,
):
    try:
        query = {}

        if brand:
            query["brand"] = brand
        if model:
            query["model"] = model
        if year:
            query["year"] = year
        if color:
            query["color"] = color
        if mileage:
            query["mileage"] = mileage
        if status:
            query["status"] = status.value

        cars = cars_collection.find(query)
        result = list(cars)

        if result:
            return result
        else:
            raise HTTPException(status_code=404, detail="No cars found based on the provided criteria")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)

