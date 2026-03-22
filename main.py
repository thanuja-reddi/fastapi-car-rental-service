from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()

# ------------------ DATABASE ------------------
cars = [
    {"id": 1, "brand": "Toyota", "model": "Innova", "price_per_day": 2000, "year": 2022, "available": True},
    {"id": 2, "brand": "Hyundai", "model": "Creta", "price_per_day": 1800, "year": 2021, "available": True},
    {"id": 3, "brand": "Honda", "model": "City", "price_per_day": 1500, "year": 2020, "available": True},
]

customers = []
rentals = []

# ------------------ MODELS ------------------
class Car(BaseModel):
    id: int
    brand: str
    model: str
    price_per_day: float = Field(gt=0)
    year: int
    available: bool = True

class Customer(BaseModel):
    id: int
    name: str = Field(min_length=2)
    license_number: str = Field(min_length=5)

class Rental(BaseModel):
    id: int
    car_id: int
    customer_id: int
    days: int = Field(gt=0)
    status: str = "booked"

# ------------------ HELPERS ------------------
def find_car(car_id):
    return next((c for c in cars if c["id"] == car_id), None)

def find_customer(customer_id):
    return next((c for c in customers if c["id"] == customer_id), None)

def find_rental(rental_id):
    return next((r for r in rentals if r["id"] == rental_id), None)

def calculate_rent(price, days):
    return price * days

# ------------------ GET APIs ------------------
@app.get("/")
def home():
    return {"message": "Welcome to Car Rental Service"}

@app.get("/cars")
def get_cars():
    return {"total": len(cars), "cars": cars}

@app.get("/cars/summary")
def summary():
    available = [c for c in cars if c["available"]]
    return {
        "total": len(cars),
        "available": len(available),
        "rented": len(cars) - len(available)
    }



# ------------------ POST APIs ------------------
@app.post("/cars", status_code=201)
def add_car(car: Car):
    cars.append(car.dict())
    return car

@app.post("/customers", status_code=201)
def add_customer(customer: Customer):
    customers.append(customer.dict())
    return customer

@app.post("/rentals", status_code=201)
def rent_car(rental: Rental):
    car = find_car(rental.car_id)
    if not car:
        raise HTTPException(404, "Car not found")

    if not car["available"]:
        raise HTTPException(400, "Car not available")

    car["available"] = False
    total = calculate_rent(car["price_per_day"], rental.days)

    new_rental = rental.dict()
    new_rental["total_price"] = total

    rentals.append(new_rental)
    return new_rental

# ------------------ CRUD ------------------
@app.put("/cars/{car_id}")
def update_car(car_id: int, price: Optional[int] = None, available: Optional[bool] = None):
    car = find_car(car_id)
    if not car:
        raise HTTPException(404, "Not found")

    if price is not None:
        car["price_per_day"] = price
    if available is not None:
        car["available"] = available

    return car

@app.delete("/cars/{car_id}")
def delete_car(car_id: int):
    car = find_car(car_id)
    if not car:
        raise HTTPException(404, "Not found")

    cars.remove(car)
    return {"message": "Car deleted"}

# ------------------ WORKFLOW ------------------
@app.put("/rentals/{id}/pickup")
def pickup(id: int):
    rental = find_rental(id)
    if not rental:
        raise HTTPException(404, "Not found")

    rental["status"] = "picked"
    return rental

@app.put("/rentals/{id}/return")
def return_car(id: int):
    rental = find_rental(id)
    if not rental:
        raise HTTPException(404, "Not found")

    car = find_car(rental["car_id"])
    car["available"] = True

    rental["status"] = "returned"
    return rental

# ------------------ ADVANCED ------------------
@app.get("/cars/search")
def search(brand: Optional[str] = None):
    if brand:
        return [c for c in cars if brand.lower() in c["brand"].lower()]
    return cars

@app.get("/cars/sort")
def sort(order: str = "asc"):
    return sorted(cars, key=lambda x: x["price_per_day"], reverse=(order == "desc"))

@app.get("/cars/page")
def paginate(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    return cars[start:start + limit]

@app.get("/cars/browse")
def browse(brand: Optional[str] = None, page: int = 1, limit: int = 2):
    result = cars
    if brand:
        result = [c for c in result if brand.lower() in c["brand"].lower()]
    start = (page - 1) * limit
    return result[start:start + limit]

@app.get("/rentals")
def get_rentals():
    return {"total": len(rentals), "rentals": rentals}

@app.put("/customers/{id}")
def update_customer(id: int, name: Optional[str] = None):
    customer = next((c for c in customers if c["id"] == id), None)
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    if name is not None:
        customer["name"] = name

    return customer

@app.delete("/rentals/{id}")
def cancel_rental(id: int):
    rental = next((r for r in rentals if r["id"] == id), None)

    if not rental:
        raise HTTPException(status_code=404, detail="Rental not found")

    rentals.remove(rental)
    return {"message": "Rental cancelled"}

@app.get("/cars/{car_id}")
def get_car(car_id: int):
    car = find_car(car_id)
    if not car:
        raise HTTPException(404, "Car not found")
    return car