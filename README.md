# Employee Management API - FastAPI Task 1

## Overview

A beginner-friendly FastAPI backend for managing employee records. Task 1 uses a temporary Python list instead of a database, so records reset when the application restarts.

## Employee Fields

- `id` - auto-generated integer
- `name`
- `email`
- `department`
- `primary_skill`
- `location`
- `work_mode` - `WFH` or `WFO`
- `is_active` - defaults to `true`
- `created_at` - generated automatically

## Technologies

- Python 3.12
- FastAPI
- Pydantic
- Uvicorn
- Swagger UI
- Git

## Project Structure

```text
FastAPI-Employee-Management/
├── app/
│   ├── __init__.py
│   ├── main.py
│   └── schemas.py
│   └── services.py
├── screenshots/
├── requirements.txt
└── README.md
```

## Installation

Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Run

```powershell
python -m uvicorn app.main:app --reload
```

API:

`http://127.0.0.1:8000`

Swagger UI:

`http://127.0.0.1:8000/docs`

## APIs

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API status |
| GET | `/health` | Health check |
| POST | `/employees` | Create employee |
| GET | `/employees` | List employees |
| GET | `/employees/{id}` | Get employee |
| PUT | `/employees/{id}` | Update employee |
| DELETE | `/employees/{id}` | Delete employee |

## Sample POST

```json
{
  "name": "Rahul",
  "email": "rahul@gmail.com",
  "department": "Development",
  "primary_skill": "Python",
  "location": "Bangalore",
  "work_mode": "WFO",
  "is_active": true
}
```

## Validation

- Required text fields cannot be empty or whitespace-only.
- Email must be valid.
- Email uniqueness is checked case-insensitively.
- `work_mode` accepts only `WFH` or `WFO`.
- Employee ID must be greater than 0.
- Missing employees return `404`.
- Duplicate emails return `409`.
- Successful creation returns `201`.

## Testing

1. Start the server.
2. Open `http://127.0.0.1:8000/docs`.
3. Use **Try it out** in Swagger UI.
4. Test POST, GET, PUT and DELETE.
5. Test validation and 404 cases.

## Data Storage

No database is used in Task 1. Data is stored in a Python list in memory and is lost after restart.

## Git

```powershell
git init
git add .
git commit -m "Completed FastAPI Employee Management Task 1"
git branch -M main
git remote add origin YOUR_GITHUB_REPOSITORY_URL
git push -u origin main
```

## Screenshots

The `screenshots` folder is included for Swagger/API screenshots. Add screenshots such as:

- Swagger UI
- Create employee
- Get all employees
- Get employee by ID
- Update employee
- Delete employee
- Validation error

## Task Completion

This project contains the completed FastAPI Employee Management Task 1 code, requirements file, README, and screenshots folder.
