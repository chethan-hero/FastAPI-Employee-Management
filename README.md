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
```

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
```

Select the database:

```sql
USE employee_db;
```

The `employees` table is automatically created when FastAPI starts.

Check the table:

```sql
SHOW TABLES;
```

## Environment Configuration

Create a `.env` file in the project root:
```env
DATABASE_URL=mysql+pymysql://root:NewPassword@123@localhost:3306/employee_db
```

If the password contains `@`, encode it as `%40`.

Example:
```env
DATABASE_URL=mysql+pymysql://root:NewPassword%40123@localhost:3306/employee_db
```

Do not commit `.env` to GitHub.

## Installation

Open PowerShell:

```powershell
cd "C:\Users\User\Desktop\FastAPI-Employee-Management"
```
Install dependencies:
```powershell
python -m pip install -r requirements.txt
```

## Run Application
```powershell
python -m uvicorn app.main:app --reload
```
Application:
```text
http://127.0.0.1:8000
```
Swagger UI:
```text
http://127.0.0.1:8000/docs
```

## API Endpoints

### Home
```text
GET /
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
```text
201 Created
```

### Get Employees
```text
GET /employees
```

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
```text
GET /employees?search=cha
```
Search is partial and case-insensitive.

## Filters

Department:
```text
GET /employees?department=Development
```
Work mode:
```text
GET /employees?work_mode=WFH
```
Active employees:
```text
GET /employees?is_active=true
```
Inactive employees:
```text
GET /employees?is_active=false
```

## Combined Filters

Example:

```text
GET /employees?search=cha&department=Development&work_mode=WFO&is_active=true
```
All supplied filters are applied together.
## Pagination
Example:
```text
GET /employees?limit=5&offset=0
```
Next page:
```text
GET /employees?limit=5&offset=5
```
Rules:
```text
limit: 1-100
offset: 0 or greater
```
Invalid offset:
```text
GET /employees?limit=10&offset=-1
```
returns:
```text
422 Unprocessable Entity
```

Employees are returned in ascending ID order.

## Response Format

```json
{
  "total": 2,
  "limit": 10,
  "offset": 0,
  "items": []
}
```

If there are no matching employees:

```json
{
  "total": 0,
  "limit": 10,
  "offset": 0,
  "items": []
}
```
The API returns `200 OK` for no matches.

## Get Employee by ID
```text
GET /employees/{employee_id}
```

Example:
```text
GET /employees/1
```
Returns `404` if the employee does not exist.

## Update Employee

```text
PUT /employees/{employee_id}
```

Example:
```json
{
  "department": "Development",
  "is_active": false
}
```
Only supplied fields are updated.
`created_at` is preserved.

## Null Validation

Explicit `null` values are rejected during update.
Invalid:
```json
{
  "email": null
}
```
or:
```json
{
  "name": null
}
```

Response:

```text
422 Unprocessable Entity
```

## Delete Employee

```text
DELETE /employees/{employee_id}
```

Returns `404` if the employee does not exist.

## Validation

Required text fields cannot contain only spaces:

- name
- department
- primary_skill
- location

Valid work modes:

```text
WFH
WFO
```

Invalid input returns:

```text
422 Unprocessable Entity
```

## Email Validation

Email must be valid and unique.

Duplicate email:

```text
409 Conflict
```

Email comparison is case-insensitive.

## Database Error Handling
Database errors are not exposed as raw SQL errors.
The API returns:

```text
Database error. Please try again.
```

Failed database operations are rolled back.

## Automatic Table Creation

The application creates missing tables when it starts:

```python
Base.metadata.create_all(bind=engine)
```

This allows a fresh `employee_db` database to create the `employees` table automatically.


## Screenshots

Swagger UI screenshots are stored in the `screenshots` folder.

Important tests include:

- Create employee
- Search
- Filters
- Combined filters
- Pagination
- No matches
- Invalid offset
- Validation errors

Screenshots should show the actual **Execute** response.

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
Check status:
```powershell
git status

Add changes:
```powershell
git add .

Commit:
```powershell
git commit -m "Fix Task 3 validation and database handling"

Push:
```powershell
git push origin main

## Security
Never commit real database passwords.
`.gitignore` should contain:

.env
.venv/
venv/
__pycache__/
*.pyc
``

Use a dummy password in `.env.example`:

DATABASE_URL=mysql+pymysql://root:NewPassword@123@localhost:3306/employee_db

## Project Status
**Task 1:** Employee CRUD
**Task 2:** MySQL + SQLAlchemy integration
**Task 3:** Search, filtering, and pagination
**Status:** Completed and ready for testing.