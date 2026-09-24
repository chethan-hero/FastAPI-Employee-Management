# FastAPI Employee Management API
A REST API for managing employee records using FastAPI, MySQL, SQLAlchemy, and Pydantic.

## Features
- Employee CRUD operations
- MySQL database integration
- SQLAlchemy ORM
- Request validation
- Case-insensitive unique email
- Search employees by name
- Filter by department
- Filter by work mode
- Filter by active status
- Pagination using limit and offset
- Automatic database table creation
- Database error handling
- Swagger UI documentation
- Git and GitHub

## Technologies

- Python 3.12+
- FastAPI
- Pydantic
- SQLAlchemy
- MySQL
- PyMySQL
- python-dotenv
- Uvicorn
- Swagger UI

## Project Structure

```text
FastAPI-Employee-Management/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
│
├── screenshots/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md


## Employee Fields

| Field | Description |
|---|---|
| id | Auto-generated ID |
| name | Employee name |
| email | Unique email |
| department | Department |
| primary_skill | Primary skill |
| location | Employee location |
| work_mode | WFH or WFO |
| is_active | Active status |
| created_at | Creation date and time |

## Database Setup

Create the MySQL database:

```sql
CREATE DATABASE employee_db;
Select the database:
```sql
USE employee_db;
The `employees` table is automatically created when FastAPI starts.
Check the table:
```sql
SHOW TABLES;

## Environment Configuration

Create a `.env` file in the project root:
```env
DATABASE_URL=mysql+pymysql://root:NewPassword%40123@localhost:3306/employee_db

## Installation
Open PowerShell:
cd "C:\Users\User\Desktop\FastAPI-Employee-Management"
Install dependencies:
python -m pip install -r requirements.txt

## Run Application
python -m uvicorn app.main:app --reload
Application:
http://127.0.0.1:8000
Swagger UI:
http://127.0.0.1:8000/docs

## API Endpoints
### Home
GET /
### Health Check

GET /health

Response:

```json
{
  "status": "healthy",
  "message": "Application is running"
}
```

### Create Employee

```text
POST /employees
```

Example:

```json
{
  "name": "Chethan",
  "email": "chethan@gmail.com",
  "department": "Development",
  "primary_skill": "Python",
  "location": "Mandya",
  "work_mode": "WFO",
  "is_active": true
}
```

Returns:
201 Created


### Get Employees
Supported query parameters:

| Parameter | Description | Default |
|---|---|---|
| search | Search employee name | None |
| department | Department filter | None |
| work_mode | WFH or WFO | None |
| is_active | Active status | None |
| limit | Records per page | 10 |
| offset | Records to skip | 0 |

## Search

Example:
GET /employees?search=cha
## Filters

Department:
GET /employees?department=Development
Work mode:
GET /employees?work_mode=WFH
Active employees:
GET /employees?is_active=true
Inactive employees:
GET /employees?is_active=false

## Combined Filters
GET /employees?search=cha&department=Development&work_mode=WFO&is_active=true
All supplied filters are applied together.

## Pagination

Example:
GET /employees?limit=5&offset=0
Next page:
GET /employees?limit=5&offset=5
Rules:
limit: 1-100
offset: 0 or greater
Invalid offset:
GET /employees?limit=10&offset=-1
returns:
422 Unprocessable Entity
Employees are returned in ascending ID order.

## Response Format

```json
{
  "total": 2,
  "limit": 10,
  "offset": 0,
  "items": []
}
If there are no matching employees:

```json
{
  "total": 0,
  "limit": 10,
  "offset": 0,
  "items": []
}
The API returns `200 OK` for no matches.

## Get Employee by ID
GET /employees/{employee_id}


Example:
GET /employees/1

Returns `404` if the employee does not exist.

## Update Employee
PUT /employees/{employee_id}
Example:

```json
{
  "department": "Development",
  "is_active": false
}
Only supplied fields are updated.
`created_at` is preserved.

## Delete Employee
DELETE /employees/{employee_id}


Returns `404` if the employee does not exist.

## Validation

Required text fields cannot contain only spaces:
- name
- department
- primary_skill
- location

Valid work modes:
WFH
WFO

Invalid input returns:
422 Unprocessable Entity

## Email Validation

Email must be valid and unique.
Duplicate email:
409 Conflict
Email comparison is case-insensitive.

## Database Error Handling

Database errors are not exposed as raw SQL errors.
The API returns:
```text
Database error. Please try again.
Failed database operations are rolled back.
## Automatic Table Creation
The application creates missing tables when it starts:
```python
Base.metadata.create_all(bind=engine)

This allows a fresh `employee_db` database to create the `employees` table automatically.

## Screenshots
- Create employee
- Search
- Filters
- Combined filters
- Pagination
- No matches
- Invalid offset
- Validation errors
## Learning Note
This project helped me learn:

- FastAPI REST API development
- Pydantic validation
- MySQL connectivity
- SQLAlchemy ORM
- CRUD operations
- Search and filtering
- Pagination
- Error handling
- Database transactions
- Swagger UI
- Git and GitHub

## Git Commands
git status
Add changes:
git add .
git commit -m "Fix Task 3 validation and database handling"
Push:
git push origin main

.gitignore` should contain:
.env
.venv/
venv/
__pycache__/
*.pyc

Summary

Task 3 extends the Employee Management API with database-backed search, filtering, and pagination while preserving the existing CRUD functionality from Task 2. The API now supports partial and case-insensitive name search, department filtering, WFH/WFO filtering, active-status filtering, combined filters, deterministic ID ordering, and limit/offset pagination using SQLAlchemy queries.



