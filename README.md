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

```powershell
git commit -m "Complete Task 2 MySQL SQLAlchemy implementation"

Set the main branch:

```powershell
git branch -M main

Add the GitHub repository:

```powershell
git remote add origin https://github.com/chethan-hero/FastAPI-Employee-Management.git
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

