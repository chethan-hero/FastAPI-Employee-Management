# Employee Management API

A FastAPI backend application for managing employee records using **Python, FastAPI, MySQL, and SQLAlchemy**.

## Project Overview

This project implements an Employee Management REST API.

In Task 2, employee records are stored in a **MySQL database** using **SQLAlchemy ORM**. Employee data remains available even after restarting the FastAPI application.

## Technologies Used

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- MySQL
- PyMySQL
- Uvicorn
- python-dotenv
- Swagger UI
- Git
- GitHub
- Visual Studio Code

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
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Employee Fields

| Field | Description |
|---|---|
| `id` | Automatically generated employee ID |
| `name` | Employee name |
| `email` | Employee email |
| `department` | Employee department |
| `primary_skill` | Primary technical skill |
| `location` | Employee location |
| `work_mode` | WFH or WFO |
| `is_active` | Employee active status |
| `created_at` | Employee creation date and time |

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/health` | Check application status |
| POST | `/employees` | Create an employee |
| GET | `/employees` | Get all employees |
| GET | `/employees/{employee_id}` | Get employee by ID |
| PUT | `/employees/{employee_id}` | Update employee |
| DELETE | `/employees/{employee_id}` | Delete employee |

## MySQL Database Setup

Create the database in MySQL:

```sql
CREATE DATABASE IF NOT EXISTS employee_db;
```

Select the database:

```sql
USE employee_db;
```

The `employees` table is created automatically by SQLAlchemy when the FastAPI application starts successfully.

Check the tables:

```sql
SHOW TABLES;
```

Check employee records:

```sql
SELECT * FROM employees;
```

## Environment Configuration

Create a `.env` file in the project root directory.

Example:

```env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/employee_db
```

If the MySQL password contains special characters, URL-encode them.

For example:

```text
@
```

must be written as:

```text
%40
```

Example:

```env
DATABASE_URL=mysql+pymysql://root:MySql%4012345@localhost:3306/employee_db
```

The `.env` file should not be uploaded to GitHub.

## Install Dependencies

Open PowerShell in the project directory:

```powershell
cd "C:\Users\User\Desktop\FastAPI-Employee-Management"
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the required packages:

```powershell
python -m pip install -r requirements.txt
```

## Run the Application

Start FastAPI using:

```powershell
python -m uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

## Swagger UI

Open the following URL in a browser:

```text
http://127.0.0.1:8000/docs
```

Swagger UI can be used to test all API endpoints.

## Health Check

Endpoint:

```text
GET /health
```

Example response:

```json
{
  "status": "healthy",
  "message": "Application is running"
}
```

## Create Employee

Endpoint:

```text
POST /employees
```

Example request:

```json
{
  "name": "Chethan",
  "email": "chethan@gmail.com",
  "department": "Development",
  "primary_skill": "Python",
  "location": "Mandya",
  "work_mode": "WFO"
}
```

The employee ID and creation date are generated automatically.

The API returns:

```text
201 Created
```

## Get All Employees

Endpoint:

```text
GET /employees
```

This returns all employees stored in the MySQL database.

## Get Employee by ID

Endpoint:

```text
GET /employees/{employee_id}
```

Example:

```text
GET /employees/1
```

If the employee does not exist, the API returns:

```text
404 Not Found
```

## Update Employee

Endpoint:

```text
PUT /employees/{employee_id}
```

Example:

```text
PUT /employees/1
```

Request:

```json
{
  "name": "Chethan Kumar",
  "email": "chethankumar@gmail.com",
  "department": "Development",
  "primary_skill": "FastAPI",
  "location": "Mandya",
  "work_mode": "WFH"
}
```

The following values are preserved during an update:

- Employee ID
- `is_active`
- `created_at`

## Delete Employee

Endpoint:

```text
DELETE /employees/{employee_id}
```

Example:

```text
DELETE /employees/1
```

Example response:

```json
{
  "message": "Employee deleted successfully"
}
```

## Validation

The API validates employee information.

### Required Fields

The following fields are required:

- Name
- Email
- Department
- Primary skill
- Location

Empty or whitespace-only values are rejected.

### Email Validation

The email must be in a valid email format.

Email addresses are normalized to lowercase.

For example:

```text
Chethan@Gmail.com
```

is stored as:

```text
chethan@gmail.com
```

### Email Uniqueness

Email addresses must be unique.

If an existing email is used, the API returns:

```text
409 Conflict
```

Example:

```json
{
  "detail": "Email already exists"
}
```

### Work Mode

Only these values are allowed:

```text
WFH
WFO
```

## Error Handling

### Invalid Employee ID

If the employee ID is zero or negative:

```text
400 Bad Request
```

Example:

```json
{
  "detail": "Employee ID must be greater than 0"
}
```

### Employee Not Found

```text
404 Not Found
```

Example:

```json
{
  "detail": "Employee not found"
}
```

### Duplicate Email

```text
409 Conflict
```

Example:

```json
{
  "detail": "Email already exists"
}
```

## Database Persistence

Employee data is stored in MySQL instead of a temporary Python list.

Therefore, employee records remain available after restarting the FastAPI application.

To verify the records:

```sql
USE employee_db;

SELECT * FROM employees;
```

## SQLAlchemy

SQLAlchemy is used as the Object Relational Mapper (ORM).

SQLAlchemy handles:

- MySQL connection
- Table creation
- Insert operations
- Select operations
- Update operations
- Delete operations
- Transactions
- Rollback

## Database Session

The application creates a database session for API requests.

The session is automatically closed after the request is completed.

## Transaction Rollback

If a database operation fails, the transaction is rolled back to prevent incomplete database changes.

## Testing

The following features can be tested using Swagger UI:

- Health check
- Create employee
- Get all employees
- Get employee by ID
- Update employee
- Delete employee
- Invalid employee ID
- Employee not found
- Duplicate email
- Invalid email
- Empty required fields
- Invalid work mode
- MySQL database persistence

## Screenshots

The `screenshots` folder contains screenshots showing:

1. Swagger UI
2. Health check
3. Create employee
4. Get employees
5. Update employee
6. Delete employee
7. MySQL database
8. Employee table and records
9. Persistence after application restart

## Git Commands

Initialize Git:

```powershell
git init
```

Check status:

```powershell
git status
```

Add files:

```powershell
git add .
```

Commit the project:

```powershell
git commit -m "Complete Task 2 MySQL SQLAlchemy implementation"
```

Set the main branch:

```powershell
git branch -M main
```

Add the GitHub repository:

```powershell
git remote add origin https://github.com/chethan-hero/FastAPI-Employee-Management.git
```

Push the project:

```powershell
git push -u origin main
```

## Security

The `.env` file contains database credentials and should not be committed to GitHub.

The `.gitignore` file includes:

```gitignore
.env
.venv/
venv/
__pycache__/
*.py[cod]
.vscode/
.idea/
.pytest_cache/
.DS_Store
Thumbs.db
```

The `.env.example` file can be used to show the required database configuration without exposing the actual password.
Employee records are stored permanently in MySQL and can be managed through the FastAPI REST API.
Employee Management API

FastAPI Employee Management - Task 2
