````markdown
# FastAPI Employee Management API

## Project Overview

This project is a FastAPI backend application developed to manage employee records.

The project was completed in three tasks:

- Task 1 - Employee CRUD using Python list
- Task 2 - MySQL database integration using SQLAlchemy
- Task 3 - Search, filtering and pagination

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
- Git
- GitHub

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
├── .gitignore
├── requirements.txt
└── README.md
````

## Task 1 - Employee CRUD

Task 1 implemented employee CRUD operations using FastAPI.

### API Endpoints

```text
POST   /employees
GET    /employees
GET    /employees/{employee_id}
PUT    /employees/{employee_id}
DELETE /employees/{employee_id}
GET    /health
```

### Employee Fields

* `id`
* `name`
* `email`
* `department`
* `primary_skill`
* `location`
* `work_mode`
* `is_active`
* `created_at`

### Features

* Create employee
* View all employees
* View employee by ID
* Update employee
* Delete employee
* Email validation
* Work mode validation
* Employee ID validation
* Health check

## Task 2 - MySQL and SQLAlchemy

Task 2 replaced temporary storage with a MySQL database.

### Database

```text
employee_db
```

### Table

```text
employees
```

SQLAlchemy ORM is used for database operations.

### Features

* MySQL database connection
* SQLAlchemy ORM
* Persistent employee records
* Auto-generated employee IDs
* Unique email validation
* Case-insensitive email checking
* Database rollback on failed operations
* Database session management
* Created date and time
* CRUD operations using MySQL

Employee records remain available after restarting the FastAPI application.

## Task 3 - Search, Filtering and Pagination

Task 3 added search, filtering and pagination to:

```text
GET /employees
```

### Query Parameters

| Parameter    | Description                                   | Default |
| ------------ | --------------------------------------------- | ------- |
| `search`     | Partial case-insensitive employee name search | None    |
| `department` | Filter by department                          | None    |
| `work_mode`  | Filter by WFH or WFO                          | None    |
| `is_active`  | Filter by active status                       | None    |
| `limit`      | Number of records to return                   | 10      |
| `offset`     | Number of records to skip                     | 0       |

### Search

Search employees by name using partial and case-insensitive matching.

Example:

```text
GET /employees?search=che
```

### Department Filter

Example:

```text
GET /employees?department=Development
```

### Work Mode Filter

Allowed values:

```text
WFH
WFO
```

Example:

```text
GET /employees?work_mode=WFH
```

### Active Status Filter

Example:

```text
GET /employees?is_active=true
```

or:

```text
GET /employees?is_active=false
```

### Combined Filters

Multiple filters can be used together.

Example:

```text
GET /employees?department=Engineering&work_mode=WFH
```

### Pagination

Pagination uses `limit` and `offset`.

Example:

```text
GET /employees?limit=3&offset=0
```

Next page:

```text
GET /employees?limit=3&offset=3
```

The API returns:

* Total matching records
* Limit
* Offset
* Employee items

Example response:

```json
{
  "total": 8,
  "limit": 3,
  "offset": 0,
  "items": []
}
```

### No Matching Records

If there are no matching employees, the API returns HTTP `200` with an empty `items` list.

Example:

```text
GET /employees?search=lohith
```

Response:

```json
{
  "total": 0,
  "limit": 10,
  "offset": 0,
  "items": []
}
```

### Offset Beyond Matching Records

If the offset exceeds the matching records, the API returns an empty `items` list while retaining the correct `total`.
### SQLAlchemy Query

Search, filtering, sorting and pagination are performed through SQLAlchemy database queries.

The application does not load all employees into a Python list for filtering.

Employees are returned in ascending order by employee ID.

## API Endpoints

### Home

```text
GET /
```

Response:

```json
{
  "message": "Employee Management API is running"
}
```

### Health Check

```text
GET /health
```

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

Example request:

```json
{
  "name": "Arun",
  "email": "arun1@gmail.com",
  "department": "Sales",
  "primary_skill": "Marketing",
  "location": "Bengaluru",
  "work_mode": "WFO",
  "is_active": true
}
```

Successful creation returns:

```text
201 Created
```
### Get Employee
```text
GET /employees/{employee_id}
```
Example:
```text
GET /employees/6
```
### Update Employee
```text
PUT /employees/{employee_id}
```
Example:
```json
{
  "department": "Development",
  "is_active": true
}
```
The `created_at` value is preserved during updates.
### Delete Employee
```text
DELETE /employees/{employee_id}
```
Example response:

```json
{
  "message": "Employee deleted successfully",
  "id": 6
}
## Environment Variables
Create a `.env` file in the project root:
DATABASE_URL=mysql+pymysql://root:NewPassword@123@localhost:3306/employee_db```


## Installation
Clone the repository:
git clone https://github.com/chethan-hero/FastAPI-Employee-Management.git
Open the project:
cd FastAPI-Employee-Management
Install dependencies:
python -m pip install -r requirements.txt
## Run the Application
Start the FastAPI application:
python -m uvicorn app.main:app --reload
Application URL:

```text
http://127.0.0.1:8000
```

## Swagger UI

Open the following URL in a browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI is used to test all API endpoints.

## Testing

The following features were tested using Swagger UI:

* Create employee
* Get all employees
* Get employee by ID
* Update employee
* Delete employee
* Health check
* Employee search
* Department filter
* Work mode filter
* Active status filter
* Combined filters
* Pagination
* No matching records
* Invalid limit
* Invalid offset
* Invalid work mode

## Screenshots

Swagger UI screenshots are stored in the `screenshots` folder.

Task 3 screenshots include:

* Search
* Department filter
* Work mode filter
* Active status filter
* Combined filters
* Pagination
* No matching records
* Invalid offset

## Git Commands

Check status:
git status
Add changes:
git add .
Commit changes:
git commit -m "Complete Task 1 Task 2 and Task 3"
Push changes:
git push origin main
## GitHub Repository

[https://github.com/chethan-hero/FastAPI-Employee-Management](https://github.com/chethan-hero/FastAPI-Employee-Management)

## Conclusion

Tasks 1, 2 and 3 of the FastAPI Employee Management project have been completed.

The application provides employee CRUD operations, MySQL database persistence, validation, search, filtering and pagination using FastAPI and SQLAlchemy.
