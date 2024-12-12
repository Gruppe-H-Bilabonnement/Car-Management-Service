# Car Management API

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)
![Postman](https://img.shields.io/badge/Postman-FF6C37?style=for-the-badge&logo=postman&logoColor=white)
![Tableau](https://img.shields.io/badge/Tableau-E97627?style=for-the-badge&logo=tableau&logoColor=white)
![Azure](https://img.shields.io/badge/Microsoft%20Azure-0078D4?style=for-the-badge&logo=microsoft-azure&logoColor=white)  

A robust, scalable Flask-based API for managing a car inventory, designed with modern Python development best practices.

## Project Overview

The Car Management API streamlines operations for managing car data, including creating, updating, and querying car records. Built with Flask, SQLite, and Docker, it follows a RESTful design pattern and includes detailed Swagger documentation for ease of use.

---

## Key Features

### Technical Highlights
- **Modern Python Stack**: Built with Flask, SQLite, and Swagger for scalable and maintainable development.
- **RESTful API Design**: Provides full CRUD operations for car data.
- **Automatic Database Initialization**: Dynamic table creation and data population from Excel files.
- **Interactive Documentation**: Swagger UI for testing and learning API endpoints.
- **Flexible Error Handling**: Standardized JSON responses for errors.

### Functional Capabilities
- Retrieve all car records
- Retrieve specific cars by ID, make, fuel type, or pickup location
- Add, update, or delete car records
- Flexible integration with external systems

---

## Architectural Design

### System Components

1. **Web Framework**: Flask
   - Lightweight, fast, and easy to extend
   - Provides routing and request handling

2. **Database**: SQLite
   - Serverless, embedded database
   - Handles data storage with automatic table creation

3. **Data Processing**: Pandas
   - Handles importing and transforming Excel data
   - Robust and flexible for cleaning data

4. **Documentation**: Swagger (via Flasgger)
   - Swagger/OpenAPI specification generaion
   - Simple testing interface for endpoints

---

## 📂 Project Structure
```
car-management-service/
│
├── app.py                   # Main application entry point
├── database/
│   └── initialization.py    # Database setup and data loading
│
├── api/
│   └── routes.py            # API endpoint definitions
│
├── repositories/
│   └── repository.py        # Database interaction methods
│
├── swagger/
│   ├── config.py            # Swagger configuration
│   └── docs/                # Swagger documentation specs
│
└── csv/
    └── Bilabonnement_2024_Clean.csv  # Source data spreadsheet
```

## API Endpoints

### Base URL: `/api/v1/car-management`

| Method | Endpoint                               | Description                                      |
|--------|---------------------------------------|--------------------------------------------------|
| GET    | `/api/v1/car-management/all`          | Retrieve all car records                        |
| GET    | `/api/v1/car-management/car/<id>`     | Retrieve a specific car by its ID               |
| GET    | `/api/v1/car-management/car/make/<id>`| Retrieve cars by their make                     |
| GET    | `/api/v1/car-management/car/fuel/<id>`| Retrieve cars by their fuel type                |
| GET    | `/api/v1/car-management/car/location/<id>`| Retrieve cars by their pickup location        |
| POST   | `/api/v1/car-management/car`          | Add a new car                                   |
| DELETE | `/api/v1/car-management/car/<id>`     | Remove a car by its ID                          |
| PATCH  | `/api/v1/car-management/car/<id>`     | Update the pickup location of a car by its ID   |

---

## Documentation

### Swagger UI
Interactive API documentation available at: `.../api/v1/docs`

---


python3 -m venv .venv
source .venv/bin/adctivate
pip install -r requirements

docker build -t car_management_service .

docker run -d -p 80:80 --name car_management_app_container car_management_service
