FastAPI Employee Management API
Project Overview

This project is a FastAPI backend application developed to manage employee records.

The project was completed in three tasks:

Task 1 – Employee CRUD using Python list
Task 2 – MySQL database integration using SQLAlchemy
Task 3 – Search, filtering and pagination
Technologies Used
Python 3.12
FastAPI
Pydantic
MySQL
SQLAlchemy
PyMySQL
Python-dotenv
Uvicorn
Swagger UI
Git
GitHub
Project Structure
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
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
Task 1 – Employee CRUD

Task 1 implemented employee CRUD operations using FastAPI.

API Endpoints
POST   /employees
GET    /employees
GET    /employees/{employee_id}
PUT    /employees/{employee_id}
DELETE /employees/{employee_id}
GET    /health
Employee Fields
id
name
email
department
primary_skill
location
work_mode
is_active
created_at
Features
Create employee
View all employees
View employee by ID
Update employee
Delete employee
Email validation
Work mode validation
Employee ID validation
Health check
Task 2 – MySQL and SQLAlchemy

Task 2 replaced temporary storage with MySQL.

Database
employee_db
Table
employees

SQLAlchemy ORM is used for database operations.

Features
MySQL database connection
SQLAlchemy ORM
Persistent employee records
Auto-generated employee IDs
Unique email validation
Case-insensitive email checking
Database rollback on failed operations
Database session management
Created date and time
CRUD operations using MySQL

Employee records remain available after restarting the FastAPI application.

Task 3 – Search, Filtering and Pagination

Task 3 added search, filtering and pagination to:

GET /employees
Query Parameters
Parameter	Description	Default
search	Partial case-insensitive employee name search	None
department	Filter by department	None
work_mode	Filter by WFH or WFO	None
is_active	Filter by active status	None
limit	Number of records to return	10
offset	Number of records to skip	0
Search
GET /employees?search=che

Search supports partial and case-insensitive employee name matching.

Department Filter
GET /employees?department=Development
Work Mode Filter

Allowed values:

WFH
WFO

Example:

GET /employees?work_mode=WFH
Active Status Filter
GET /employees?is_active=true

or:

GET /employees?is_active=false
Combined Filters

Multiple filters can be used together.

Example:

GET /employees?department=Engineering&work_mode=WFH
Pagination

Pagination uses limit and offset.

Example:

GET /employees?limit=3&offset=0

Next page:

GET /employees?limit=3&offset=3

Response format:

{
  "total": 8,
  "limit": 3,
  "offset": 0,
  "items": []
}
No Matching Records

If no employees match the search or filters, the API returns HTTP 200 with an empty items list.

Example:

GET /employees?search=ZZZZZ

Response:

{
  "total": 0,
  "limit": 10,
  "offset": 0,
  "items": []
}
Offset Beyond Matching Records

If the offset exceeds the matching records, the API returns an empty items list while retaining the correct total.

Validation

limit must be between 1 and 100.

GET /employees?limit=0

offset cannot be negative.

GET /employees?offset=-1

Only WFH and WFO are accepted.

GET /employees?work_mode=REMOTE
SQLAlchemy Query

Search, filtering, sorting and pagination are performed through SQLAlchemy database queries.

The application does not load all employees into a Python list for filtering.

Employees are returned in ascending order by employee ID.

API Endpoints
Home
GET /

Response:

{
  "message": "Employee Management API is running"
}
Health Check
GET /health

Response:

{
  "status": "healthy",
  "message": "Application is running"
}
Create Employee
POST /employees

Example:

{
  "name": "Arun",
  "email": "arun1@gmail.com",
  "department": "Sales",
  "primary_skill": "Marketing",
  "location": "Bengaluru",
  "work_mode": "WFO",
  "is_active": true
}

Successful creation returns:

201 Created
Get Employee
GET /employees/{employee_id}

Example:

GET /employees/6
Update Employee
PUT /employees/{employee_id}

Example:

{
  "department": "Development",
  "is_active": true
}

The created_at value is preserved during updates.

Delete Employee
DELETE /employees/{employee_id}

Example response:

{
  "message": "Employee deleted successfully",
  "id": 6
}
Environment Variables

Create a .env file in the project root:

DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/employee_db

Replace YOUR_PASSWORD with your MySQL password.
The .env file should not be committed to GitHub.

Installation
Clone the repository:
git clone https://github.com/chethan-hero/FastAPI-Employee-Management.git

Open the project:

cd FastAPI-Employee-Management

Install dependencies:

python -m pip install -r requirements.txt
Run the Application
python -m uvicorn app.main:app --reload

Application URL:

http://127.0.0.1:8000
Swagger UI

Open the following URL:

http://127.0.0.1:8000/docs

Swagger UI is used to test all API endpoints.

Testing

The following features were tested using Swagger UI:

Create employee
Get all employees
Get employee by ID
Update employee
Delete employee
Health check
Employee search
Department filter
Work mode filter
Active status filter
Combined filters
Pagination
No matching records
Invalid limit
Invalid offset
Invalid work mode
Screenshots

Swagger UI screenshots are stored in the screenshots folder.

Task 3 screenshots include:

Search
Department filter
Work mode filter
Active status filter
Combined filters
Pagination
No matching records
Invalid offset

Git Commands
Check status:
git status
Add changes:
git add .
git push origin main


Conclusion
Tasks 1, 2 and 3 of the FastAPI Employee Management project have been completed.
The application provides employee CRUD operations, MySQL database persistence, validation, search, filtering and pagination using FastAPI and SQLAlchemy
