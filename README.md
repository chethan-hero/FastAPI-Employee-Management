# FastAPI Employee Management System

## 1. Project Overview

A REST API application built with Python, FastAPI, MySQL, SQLAlchemy,
and Pydantic. It manages employees and their assigned work items,
including CRUD operations, searching, filtering, pagination, status
transitions, and employee work-item summaries.

Task 5 adds controlled work-item status transitions and an employee
work-item summary endpoint.

## 2. Technologies Used

-   Python 3.12+
-   FastAPI and Pydantic
-   SQLAlchemy ORM
-   MySQL and PyMySQL
-   Uvicorn and python-dotenv
-   Swagger UI
-   Git, GitHub, and Visual Studio Code

## 3. Project Structure

``` text
FastAPI-Employee-Management/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
├── screenshots/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

-   `main.py`: API routes and HTTP request/response handling.
-   `database.py`: MySQL connection and SQLAlchemy sessions.
-   `models.py`: Database tables and relationships.
-   `schemas.py`: Request validation and response schemas.
-   `services.py`: Business rules and database operations.
-   `.env`: Local database configuration; do not commit this file.
-   `.env.example`: Example environment variables with placeholder
    values.

## 4. Features

### Employee Management

-   Create, retrieve, update, and delete employees.
-   Validate employee data and prevent duplicate email addresses.
-   Search by name; filter by department, work mode, and active status.
-   Support pagination.

### Work-Item Management

-   Create, retrieve, update, and delete work items.
-   Assign and reassign work items to employees.
-   Search by title and filter by employee, status, and priority.
-   Validate work-item information and status transitions.

### Employee Work-Item Summary

-   Count work items currently assigned to an employee.
-   Count `TODO`, `IN_PROGRESS`, and `COMPLETED` work items.
-   Calculate counts using SQLAlchemy database aggregation.
-   Return zero counts for an existing employee with no work items.
-   Return HTTP 404 when the employee does not exist.
-   Reflect status changes, reassignment, and deletion in subsequent
    summaries.

## 5. Work-Item Statuses and Priorities

### Statuses

  Status          Description
  --------------- ------------------------------
  `TODO`          Work has not yet progressed.
  `IN_PROGRESS`   Work is being performed.
  `COMPLETED`     Work is complete.

### Priorities

  Priority   Description
  ---------- -----------------------
  `LOW`      Low-priority work.
  `MEDIUM`   Normal-priority work.
  `HIGH`     High-priority work.

The default status is `TODO`; the default priority is `MEDIUM`. The
service layer should enforce the configured transition rules
consistently for PUT and PATCH. Rejected updates must not modify the
stored record. Requesting the current status again should follow the
same-status rule implemented by the service.

## 6. Employee Work-Item Summary API

**Endpoint**

``` http
GET /employees/{employee_id}/work-items/summary
```

**Example request**

``` http
GET /employees/1/work-items/summary
```

**Example response**

``` json
{
  "total_work_items": 5,
  "todo": 2,
  "in_progress": 2,
  "completed": 1
}
```

  -----------------------------------------------------------------------
  Field                               Description
  ----------------------------------- -----------------------------------
  `total_work_items`                  Total work items currently assigned
                                      to the employee.

  `todo`                              Number of `TODO` items.

  `in_progress`                       Number of `IN_PROGRESS` items.

  `completed`                         Number of `COMPLETED` items.
  -----------------------------------------------------------------------

Business rules:

1.  Count only work items currently assigned to the requested employee.
2.  Calculate counts in the database using SQLAlchemy.
3.  The status counts must add up to `total_work_items`.
4.  An existing employee with no work items receives zero for every
    count.
5.  A nonexistent employee receives HTTP 404.
6.  Deleted items are excluded; reassigned items count for their current
    employee.
7.  Status changes are reflected in subsequent summary requests.

Example for an employee without work items:

``` json
{
  "total_work_items": 0,
  "todo": 0,
  "in_progress": 0,
  "completed": 0
}
```

## 7. Work-Item Update APIs

-   `PUT /work-items/{work_item_id}` --- updates fields supported by the
    PUT schema.
-   `PATCH /work-items/{work_item_id}` --- updates fields supported by
    the PATCH schema.

Test valid forward transitions, prohibited backward transitions, skipped
transitions, same-status requests, invalid status values, null or
missing status where required, and PUT requests that omit status. Ensure
rejected transitions leave the record unchanged.

## 8. Validation and Error Handling

-   Required fields cannot be empty.
-   Invalid status, priority, and work-mode values are rejected.
-   Invalid employee IDs are rejected.
-   Duplicate employee email addresses are prevented.
-   Missing employees and work items return HTTP 404.
-   Invalid request data returns HTTP 422.
-   Rejected transitions do not change existing records.
-   Database changes should be committed only after validation succeeds.

## 9. Database Design

### Employees table

Stores ID, name, email, department, primary skill, location, work mode,
active status, and creation timestamp.

### Work items table

Stores ID, title, description, employee ID, status, priority, due date,
and creation timestamp.

The `employee_id` field in `work_items` references the assigned employee
through a foreign key.

## 10. Database Configuration

Create a `.env` file in the project root:

``` env
DATABASE_URL=mysql+pymysql://root:YOUR_PASSWORD@localhost:3306/employee_db
```

Replace `YOUR_PASSWORD` with your local MySQL password. Do not commit
`.env` to GitHub. Keep `.env.example` with placeholder values.

## 11. Installation and Setup

### Step 1: Clone the repository

``` powershell
git clone https://github.com/chethan-hero/FastAPI-Employee-Management.git
```

### Step 2: Enter the project folder

``` powershell
cd FastAPI-Employee-Management
```

### Step 3: Create and activate a virtual environment

``` powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Step 4: Install dependencies

``` powershell
python -m pip install -r requirements.txt
```

### Step 5: Configure MySQL

Ensure MySQL is running, then create the database if needed:

``` sql
CREATE DATABASE employee_db;
```

Configure `DATABASE_URL` in `.env` and ensure the application
initializes the required tables.

### Step 6: Start the application

``` powershell
python -m uvicorn app.main:app --reload
```

## 12. Application URLs

-   Application: http://127.0.0.1:8000
-   Swagger UI: http://127.0.0.1:8000/docs
-   Health check: http://127.0.0.1:8000/health

Use Swagger UI to test employee endpoints, work-item endpoints, status
transitions, and summary responses.

## 13. Testing Checklist

### Status transitions

-   Valid forward transitions.
-   Prohibited backward and skipped transitions.
-   Requesting the current status again.
-   Invalid, null, or missing status values.
-   PUT requests that omit status.
-   Rejected updates leave stored data unchanged.

### Employee summary

-   Employee with multiple work items.
-   Employee with no work items.
-   Nonexistent employee.
-   Summary before and after status changes.
-   Summary before and after reassignment or deletion.
-   Status counts add up to the total.

### Regression and persistence

-   Employee and work-item CRUD operations.
-   Search, filtering, combined filters, and pagination.
-   Request validation.
-   Data remains correct after restarting the application.

## 14. HTTP Status Codes

  Code                          Meaning
  ----------------------------- ---------------------------------------
  `200 OK`                      Request completed successfully.
  `201 Created`                 Resource created successfully.
  `204 No Content`              Resource deleted successfully.
  `404 Not Found`               Employee or work item does not exist.
  `422 Unprocessable Entity`    Request validation failed.
  `500 Internal Server Error`   Unexpected server-side error.

## 15. Task 5 Objectives

1.  Implement controlled work-item status transitions.
2.  Reuse status-transition logic across PUT and PATCH.
3.  Separate request validation, business rules, and route handling.
4.  Calculate employee work-item summaries using SQLAlchemy.
5.  Count only currently assigned work items.
6.  Handle missing employees and work items correctly.
7.  Prevent rejected updates from modifying existing data.
8.  Preserve database changes across application restarts.
9.  Maintain compatibility with existing APIs.

## 16. What I Learned

-   Building REST APIs using FastAPI.
-   Validating requests using Pydantic.
-   Connecting FastAPI to MySQL.
-   Using SQLAlchemy ORM, primary keys, foreign keys, and relationships.
-   Implementing CRUD, search, filtering, and pagination.
-   Applying service-layer business rules and reusing them across
    routes.
-   Validating status transitions and calculating aggregate counts.
-   Handling HTTP errors and testing APIs in Swagger UI.
-   Checking database persistence and managing code with Git and GitHub.

## 17. Difficulties Faced

I faced difficulties setting up the MySQL connection, configuring
database credentials, handling duplicate email validation, understanding
SQLAlchemy operations, and testing APIs in Swagger UI.

In Task 3, I worked through pagination response structures, combined
filters, and query-parameter validation. In Task 4, I worked through
Employee--WorkItem relationships, assigned employee responses,
filtering, pagination, and validation of invalid status, priority, and
employee values.

## 18. Project Status

-   **Task 1:** Employee Management API.
-   **Task 2:** MySQL integration and SQLAlchemy persistence.
-   **Task 3:** Employee search, filtering, and pagination.
-   **Task 4:** Work-item CRUD, employee assignment and reassignment,
    relationships, search, filtering, pagination, validation, and error
    handling.
-   **Task 5:** Work-item status transitions and employee work-item
    summary API. Confirm that the implementation is tested in the Task 5
    branch before marking this task complete.

## 19. GitHub Repository

-   **Repository:**
    https://github.com/chethan-hero/FastAPI-Employee-Management
-   **Task 5 branch:**
    https://github.com/chethan-hero/FastAPI-Employee-Management/tree/task-5
-   **Local API documentation:** http://127.0.0.1:8000/docs
