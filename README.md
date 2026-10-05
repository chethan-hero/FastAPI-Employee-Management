# FastAPI Employee Management

## Project Description

This project is a FastAPI backend for managing employee records and work items. Employee and work item records are stored in a MySQL database using SQLAlchemy. The records remain available even after the application is restarted.

## Technologies Used

- Python 3.12
- FastAPI
- Pydantic
- MySQL
- SQLAlchemy
- PyMySQL
- Uvicorn
- Swagger UI
- Git
- GitHub

## Employee Fields

- ID
- Name
- Email
- Department
- Primary Skill
- Location
- Work Mode
- Is Active
- Created At

## Employee APIs

- `POST /employees`
- `GET /employees`
- `GET /employees/{id}`
- `PUT /employees/{id}`
- `DELETE /employees/{id}`
- `GET /health`

## Employee Validation

- Required employee fields are validated.
- Empty or whitespace-only required fields are rejected.
- Email format is validated.
- Duplicate email is not allowed.
- Email uniqueness is checked without treating uppercase and lowercase as different.
- Work mode accepts `WFH` or `WFO`.
- Employee ID must be greater than 0.
- 404 error is returned when an employee is not found.
- Employee IDs are generated automatically by the database.
- `is_active` is set to `true` by default.
- `created_at` is generated when an employee is created and preserved during updates.
- Failed database changes are rolled back so that later requests can continue working.

# Task 3 - Search, Filtering and Pagination

The `GET /employees` endpoint supports searching, filtering and pagination.

## Query Parameters

- `search` - Searches employees by name using partial and case-insensitive matching.
- `department` - Filters employees by department.
- `work_mode` - Filters employees by WFH or WFO.
- `is_active` - Filters employees by active or inactive status.
- `limit` - Maximum number of records to return. Default is 10. Allowed values are 1 to 100.
- `offset` - Number of records to skip. Default is 0. Negative values are not allowed.

## Example Request

```text
GET /employees?department=Engineering&work_mode=WFH&limit=5&offset=0
