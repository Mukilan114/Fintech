# Finance Data Processing and Access Control Backend

## Overview

This project is a backend system developed for managing financial data and user access control. It simulates a finance dashboard where users with different roles interact with financial records based on their permissions.

The system focuses on clean API design, structured data handling, and role-based access logic.

## Tech Stack

* Python
* FastAPI
* SQLite
* Uvicorn


## Features

### 1. User and Role Management

* Create users with roles (viewer, analyst, admin)
* Update user roles
* Activate or deactivate users
* Basic validation for unique email and valid roles


### 2. Financial Records Management

* Add financial records (income / expense)
* Store details such as amount, category, date, and description
* Link each record to a user
* Retrieve all records


### 3. Filtering Support

* Filter records by type (income or expense)
* Filter records by category



### 4. Dashboard Summary APIs

* Total income calculation
* Total expense calculation
* Net balance computation
* Category-wise aggregation
* Recent transactions


## API Endpoints

### User APIs

* POST `/users` → Create user
* GET `/users` → Get all users
* PUT `/users/{id}/role` → Update role
* PUT `/users/{id}/status` → Update status


### Record APIs

* POST `/records` → Add record
* GET `/records` → Get all records
* GET `/records/filter` → Filter records


### Summary APIs

* GET `/summary/income`
* GET `/summary/expense`
* GET `/summary/net`
* GET `/summary/category`
* GET `/summary/recent`


## How to Run

1 . Clone or download the project
2 . Create and activate virtual environment
3.python -m venv venv .\venv\Scripts\Activate.ps1  
4.pip install fastapi uvicorn pydantic
5.uvicorn main:app --reload
6.http://127.0.0.1:8000/docs


## Assumptions

* Authentication is simplified (no login system implemented)
* User identity is passed directly in requests
* SQLite is used for simplicity instead of a full-scale database

## Design Approach

The project is structured to keep logic simple and readable. User management and financial record handling are separated logically within the application. Validation and error handling are included to ensure reliable API behavior.

