# 🚗 FastAPI Car Rental Service

## 📌 Project Overview
This project is a fully functional Car Rental Backend System built using FastAPI.  
It allows users to manage cars, customers, and rentals through REST APIs.

The system demonstrates real-world backend development concepts including CRUD operations, workflows, and advanced API features.

---

## 🚀 Features Implemented

### 🔹 Basic APIs (GET)
- Home route
- Get all cars
- Get car by ID
- Get all rentals
- Cars summary (total, available, rented)

### 🔹 POST APIs with Validation
- Add new car
- Add customer
- Rent a car
- Pydantic validation with constraints

### 🔹 CRUD Operations
- Update car details
- Delete car
- Update customer
- Cancel rental

### 🔹 Multi-Step Workflow
- Rent Car → Pickup → Return
- Tracks rental status dynamically

### 🔹 Advanced APIs
- Search cars by brand
- Sort cars by price
- Pagination
- Combined browsing (search + pagination)

---

## 🛠️ Tech Stack
- Python
- FastAPI
- Uvicorn
- Pydantic

---

## ▶️ How to Run the Project

### 1. Install dependencies
pip install -r requirements.txt

### 2. Run the server
uvicorn main:app --reload

### 3. Open Swagger UI
http://127.0.0.1:8000/docs

---

## 📂 Project Structure

fastapi-car-rental-service/
│
├── main.py
├── requirements.txt
├── README.md
└── screenshots/

---

## 📸 API Testing

All APIs are tested using Swagger UI.

Screenshots for all 20 tasks are included in the screenshots/ folder


## 🧠 Key Learnings

- Designing RESTful APIs using FastAPI
- Using Pydantic for request validation
- Implementing CRUD operations
- Handling multi-step workflows
- Applying search, sorting, and pagination
- Testing APIs using Swagger UI



## 🙏 Acknowledgement
Grateful for the learning opportunity provided by Innomatics Research Labs.

---

## 📌 Conclusion
This project demonstrates strong backend development skills using FastAPI and covers real-world API design patterns.