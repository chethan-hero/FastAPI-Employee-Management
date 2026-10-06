Employee & Work Item Management API

A production-ready REST API to manage employees and their assigned work items, built using FastAPI, SQLAlchemy, and MySQL. Data is permanently stored in a relational database, persists across server restarts, and demonstrates one-to-many database relationships with referential integrity.

Technologies Used

Language: Python 3.12

Framework: FastAPI

Database: MySQL 8+

ORM: SQLAlchemy 2.0

Validation: Pydantic

Database Driver: PyMySQL

Server: Uvicorn

API Documentation: Swagger UI

Version Control: Git & GitHub

Features

Employee Management

Create, read, update and delete employees

Email format and uniqueness validation

WFH / WFO work mode validation

Active / inactive employee status

Automatic employee ID and creation timestamp

Search, Filtering & Pagination

The GET /employees endpoint supports:

Partial and case-insensitive name search

Department filtering

Work mode filtering

Active / inactive filtering

Combined filters

Pagination using limit and offset

Total record count before pagination

Work Item Management

Create, read, update and delete work items

Assign and reassign work items to employees

Search work items by title

Filter by employee, status and priority

Combined filtering and pagination

Work Item Status

TODO

IN_PROGRESS

COMPLETED

Work Item Priority

LOW

MEDIUM

HIGH

Project Structure

FastAPI-Employee-Management/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
│
├── screenshots/
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt

Database Design

Employees Table

Field

Description

id

Primary key

name

Employee name

email

Unique employee email

department

Employee department

primary_skill

Main skill

location

Employee location

work_mode

WFH or WFO

is_active

Active employee status

created_at

Creation date and time

Work Items Table

Field

Description

id

Primary key

title

Work item title

description

Optional description

employee_id

Foreign key to employees

status

TODO, IN_PROGRESS or COMPLETED

priority

LOW, MEDIUM or HIGH

due_date

Optional due date

created_at

Creation date and time

Database Relationship

A work item belongs to an employee through the employee_id foreign key.

employees.id
     ▲
     │
     │ one-to-many
     │
work_items.employee_id

One employee can have multiple work items.

Each work item belongs to one employee.

SQLAlchemy relationships connect the two models.

The foreign key maintains referential integrity.

API Endpoints

Employee APIs

Method

Endpoint

Description

POST

/employees

Create employee

GET

/employees

Get employees

GET

/employees/{id}

Get employee by ID

PUT

/employees/{id}

Update employee

DELETE

/employees/{id}

Delete employee

GET

/health

Health check

Work Item APIs

Method

Endpoint

Description

POST

/work-items

Create work item

GET

/work-items

Get work items

GET

/work-items/{work_item_id}

Get work item

PUT

/work-items/{work_item_id}

Update work item

DELETE

/work-items/{work_item_id}

Delete work item

Query Parameters

Employees

search
department
work_mode
is_active
limit
offset

Example:

GET /employees?department=Development&work_mode=WFO&limit=10&offset=0

Work Items

search
employee_id
status
priority
limit
offset

Example:

GET /work-items?employee_id=2&status=TODO&priority=MEDIUM&limit=10&offset=0

Validation

The API validates:

Required fields

Empty and whitespace-only fields

Email format

Duplicate email addresses

Employee IDs

Work modes

Work item titles

Work item status

Work item priority

Pagination values

Assigned employee existence

Invalid requests return validation errors. A 404 Not Found response is returned when an employee or work item does not exist.

Primary Key

A primary key uniquely identifies each record in a database table.

employees.id
work_items.id

Foreign Key

A foreign key connects one database table to another.

work_items.employee_id → employees.id

The employee_id identifies the employee assigned to the work item.

CRUD Operations

CRUD means:

Create

Read

Update

Delete

Employee and Work Item APIs implement CRUD operations using FastAPI and SQLAlchemy.

Database Setup

Create a MySQL database:

CREATE DATABASE employee_db;

Configure the local .env file:

DATABASE_URL=mysql+pymysql://root:YourPassword@localhost:3306/employee_db

Do not commit your real database password to GitHub.

The application uses SQLAlchemy and PyMySQL to connect to MySQL. The employees and work_items tables are created from the SQLAlchemy models when the application starts.

Running the Project

1. Create virtual environment

python -m venv .venv

2. Activate virtual environment

PowerShell:

.venv\Scripts\Activate.ps1

3. Install dependencies

pip install -r requirements.txt

4. Start FastAPI

python -m uvicorn app.main:app --reload

Application:

http://127.0.0.1:8000

Swagger UI

FastAPI automatically provides Swagger UI for API testing.

http://127.0.0.1:8000/docs

Swagger UI was used to test:

Employee CRUD

Employee search and filtering

Employee pagination

Work item CRUD

Work item assignment and reassignment

Work item search and filtering

Combined filters

Validation errors

404 errors

Delete operations

Database Error Handling

Database operations use transactions.

If an operation fails:

The error is caught.

The transaction is rolled back.

The session remains usable.

An appropriate API error response is returned.

Data Persistence

MySQL provides persistent storage.

Create Employee
      ↓
Create Work Item
      ↓
Stop FastAPI Server
      ↓
Start FastAPI Server
      ↓
Request Employee / Work Item
      ↓
Data is still available

Testing

Task 3

Employee name search

Department filtering

Work mode filtering

Active / inactive filtering

Combined filters

Pagination

No matching results

Invalid limit

Negative offset

Invalid work mode

Task 4

Create work item

Non-existing employee validation

Get all work items

Get work item by ID

Search by title

Employee filtering

Status filtering

Priority filtering

Combined filters

Pagination

Update work item

Reassign work item

Invalid status and priority

Blank title validation

Delete work item

Verify deleted item returns 404

Verify persistence after restart

What I Learned

Through this project, I learned how to:

Build REST APIs using FastAPI.

Use Pydantic for request validation.

Connect FastAPI to MySQL.

Use SQLAlchemy ORM.

Create database models.

Create primary and foreign keys.

Create SQLAlchemy relationships.

Implement CRUD operations.

Implement search and filtering.

Implement combined filters.

Implement pagination.

Count records before pagination.

Validate query parameters.

Handle HTTP status codes.

Handle database exceptions.

Use transactions and rollback.

Test APIs using Swagger UI.

Verify database persistence.

Use Git and GitHub.

Document a project using README.md.

Difficulties

I faced difficulties while:

Setting up the MySQL connection.

Configuring database connection details.

Handling duplicate email validation.

Understanding SQLAlchemy operations.

Testing APIs using Swagger UI.

Implementing pagination.

Combining multiple filters.

Implementing the Employee and WorkItem relationship.

Handling assigned employee responses.

Validating invalid status, priority and employee values.

Project Status

Task 1

Employee Management API implemented.

Task 2

MySQL database integration and SQLAlchemy persistence implemented.

Task 3

Employee search, filtering and pagination implemented.

Task 4

Work Item Management API implemented with:

Work item CRUD

Employee assignment

Employee reassignment

Foreign key relationship

SQLAlchemy relationship

Search

Filtering

Combined filters

Pagination

Validation

Error handling

Database persistence

Conclusion

This project demonstrates a FastAPI backend connected to MySQL using SQLAlchemy.

The application supports employee management and work item management with validation, CRUD operations, search, filtering, pagination, database relationships, error handling and persistent storage.

The project was tested using Swagger UI and maintained using Git and GitHub.
