# FastAPI Employee Management API

## Project Overview

This project is a FastAPI backend application for managing employee records.

The project includes:

- Employee CRUD operations
- MySQL database integration
- SQLAlchemy ORM
- Employee search
- Employee filtering
- Pagination
- Request validation
- Swagger UI documentation

## Technologies Used

- Python 3.12
- FastAPI
- Pydantic
- MySQL
- SQLAlchemy
- PyMySQL
- Python-dotenv
- Uvicorn
- Swagger UI
- Git and GitHub

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
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
Employee Fields
id - Auto-generated employee ID
name - Employee name
email - Unique employee email
department - Employee department
primary_skill - Primary skill
location - Employee location
work_mode - WFH or WFO
is_active - Employee active status
created_at - Employee creation date and time
API Endpoints
Home
GET /
Health Check
GET /health
Create Employee
POST /employees
Get All Employees
GET /employees
Get Employee by ID
GET /employees/{employee_id}
Update Employee
PUT /employees/{employee_id}
Delete Employee
DELETE /employees/{employee_id}

Task 3 - Search, Filtering and Pagination

The GET /employees API supports search, filtering, and pagination.

Query Parameters
Parameter	Description	Default
search	Partial case-insensitive employee name search	None
department	Filter by department	None
work_mode	Filter by WFH or WFO	None
is_active	Filter by active status	None
limit	Number of records to return	10
offset	Number of records to skip	0
Search

Search employee names using partial and case-insensitive matching.

Example:

GET /employees?search=che
Department Filter

Example:

GET /employees?department=Development
Work Mode Filter

Allowed values:

WFH
WFO

Example:

GET /employees?work_mode=WFH
Active Status Filter

Example:

GET /employees?is_active=true

or

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

The total value shows the total number of matching records before pagination.

Response Format
{
  "total": 8,
  "limit": 3,
  "offset": 0,
  "items": []
}
No Matching Records

If no employee matches the search or filters, the API returns HTTP 200.

Example:

GET /employees?search=ZZZZZ

Response:

{
  "total": 0,
  "limit": 10,
  "offset": 0,
  "items": []
}
Validation
Invalid Limit

limit must be between 1 and 100.

GET /employees?limit=0
Invalid Offset

offset cannot be negative.

GET /employees?offset=-1
Invalid Work Mode

Only WFH and WFO are accepted.

GET /employees?work_mode=REMOTE
Database

The application uses MySQL with SQLAlchemy.

Database:

employee_db

Table:

employees

Employee records are stored permanently in MySQL and remain available after restarting the application.

Environment Variables

Create a .env file in the project root:

DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/employee_db

Replace YOUR_PASSWORD with your MySQL password.

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

Open:

http://127.0.0.1:8000/docs

Swagger UI is used to test all API endpoints.

Testing

The following Task 3 tests were performed:

Employee search
Department filtering
Work mode filtering
Active status filtering
Combined filters
Pagination
No matching records
Invalid limit
Invalid offset
Invalid work mode
What I Learned
FastAPI API development
Query parameters
Search and filtering
Pagination using limit and offset
SQLAlchemy database queries
MySQL database integration
Pydantic validation
Swagger UI testing
Git and GitHub
Difficulties Faced
Connecting FastAPI with MySQL
Configuring SQLAlchemy
Handling database sessions
Implementing search and filters
Implementing pagination
Validating query parameters
Testing API responses in Swagger UI
Managing screenshots with Git
Git Commands
git status
git add .
git commit -m "Complete Task 3 employee search filter and pagination"
git push origin main
GitHub Repository
https://github.com/chethan-hero/FastAPI-Employee-Management
Conclusion

The Employee Management API supports employee CRUD operations, MySQL database persistence, employee search, filtering, and pagination using FastAPI and SQLAlchemy.
