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

## Project Structure

```text
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
│   ├── Task 3 screenshots
│   └── Task 4 screenshots
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

## Task 3 Testing

The following scenarios were tested using Swagger UI:

- Employee name search
- Department filtering
- Work mode filtering
- Active/inactive filtering
- Combined filters
- Partial name search
- Pagination using limit and offset
- No matching results
- Offset greater than the matching records
- Invalid limit values
- Negative offset validation
- Invalid work mode validation

Search, filtering and pagination are performed using SQLAlchemy queries.

# Task 4 - Work Item Management

Task 4 adds work item management to the Employee Management API.

Each work item is assigned to an existing employee using a foreign key relationship.

## Work Item Fields

- ID
- Title
- Description
- Employee ID
- Status
- Priority
- Due Date
- Created At
- Assigned Employee

## Work Item Status

- `TODO`
- `IN_PROGRESS`
- `COMPLETED`

## Work Item Priority

- `LOW`
- `MEDIUM`
- `HIGH`

## Work Item APIs

- `POST /work-items`
- `GET /work-items`
- `GET /work-items/{work_item_id}`
- `PUT /work-items/{work_item_id}`
- `DELETE /work-items/{work_item_id}`

## Task 4 Query Parameters

The `GET /work-items` endpoint supports search, filtering and pagination.

- `search` - Searches work items by title using partial and case-insensitive matching.
- `employee_id` - Filters work items by assigned employee.
- `status` - Filters work items by status.
- `priority` - Filters work items by priority.
- `limit` - Maximum number of records to return. Default is 10. Allowed values are 1 to 100.
- `offset` - Number of records to skip. Default is 0. Negative values are not allowed.

### Example Request

```text
GET /work-items?employee_id=2&status=TODO&priority=MEDIUM&limit=10&offset=0
```

## Work Item Validation

- Title is required.
- Empty or whitespace-only titles are rejected.
- Employee ID must be greater than 0.
- Assigned employee must exist.
- Status accepts `TODO`, `IN_PROGRESS` or `COMPLETED`.
- Priority accepts `LOW`, `MEDIUM` or `HIGH`.
- Work item ID must be greater than 0.
- 404 error is returned when a work item or employee is not found.
- Invalid status or priority returns a validation error.
- Database changes are rolled back when a database error occurs.

## Employee Deletion Behavior

When an employee is deleted, all work items assigned to that employee are also deleted automatically.

This cascade delete behavior ensures that:

Assigned work items do not remain without an employee.
No orphaned work items are left in the database.
The employee and their assigned work items are removed together.
Database relationships remain consistent.

Example: If Employee ID 5 has 3 assigned work items, deleting Employee ID 5 will also delete those 3 work items automatically.
## Employee and Work Item Relationship

A work item belongs to an employee through the `employee_id` foreign key.

The `work_items.employee_id` field references the `employees.id` field.

SQLAlchemy relationships connect the Employee and WorkItem models.

- Each employee can have multiple work items.
- Each work item belongs to one employee.

Each work item response also returns the assigned employee's:

- ID
- Name
- Email

## Task 4 Testing

The following scenarios were tested using Swagger UI:

- Create work item
- Create work item with non-existing employee
- Get all work items
- Get work item by ID
- Search by title
- Filter by employee ID
- Filter by status
- Filter by priority
- Combined filters
- Pagination using limit and offset
- Update work item
- Reassign work item to another employee
- Invalid status validation
- Invalid priority validation
- Blank title validation
- Missing work item validation
- Delete work item
- Verify deleted work item returns 404
- Verify data remains available after application restart
- Verify existing employee APIs continue working

Search, filtering, pagination and ordering are performed using SQLAlchemy queries.

# Database Setup

Create a MySQL database named `employee_db`.

The application uses SQLAlchemy and PyMySQL to connect to MySQL and perform database operations.

The `employees` and `work_items` tables are created using the SQLAlchemy models when the application starts.

The email field has a database-level unique constraint.

The `work_items.employee_id` field is a foreign key that references the `employees.id` field.

Database sessions are closed after use.

## Database Configuration

Create a local `.env` file in the project root and add the database connection details.

```env
DATABASE_URL=mysql+pymysql://root:YourPassword@localhost:3306/employee_db
```

## Employees Table

The `employees` table stores employee information.

### Important Fields

- `id` - Primary key
- `name` - Employee name
- `email` - Unique employee email
- `department` - Employee department
- `primary_skill` - Main skill
- `location` - Employee location
- `work_mode` - WFH or WFO
- `is_active` - Employee active status
- `created_at` - Employee creation date and time

## Work Items Table

The `work_items` table stores work assigned to employees.

### Important Fields

- `id` - Primary key
- `title` - Work item title
- `description` - Work item description
- `employee_id` - Foreign key to employees
- `status` - TODO, IN_PROGRESS or COMPLETED
- `priority` - LOW, MEDIUM or HIGH
- `due_date` - Optional due date
- `created_at` - Work item creation date and time

# Primary Key

A primary key uniquely identifies each record in a database table.

For example:

- `employees.id`
- `work_items.id`

Each employee and work item has a unique ID.

# Foreign Key

A foreign key connects one database table to another table.

In this project:

```text
work_items.employee_id
          ↓
employees.id
```

The `employee_id` in the `work_items` table identifies the employee assigned to the work item.

# SQLAlchemy Relationship

SQLAlchemy relationships allow the application to work with related database records using Python objects.

In this project:

```text
Employee
   │
   └── WorkItem
       ├── title
       ├── status
       ├── priority
       └── employee_id
```

- One employee can have multiple work items.
- A work item belongs to one employee.

# CRUD Operations

CRUD means:

- **Create**
- **Read**
- **Update**
- **Delete**

Employee and WorkItem APIs implement CRUD operations using FastAPI and SQLAlchemy.

# Database Error Handling

Database operations are handled using transactions.

If a database operation fails:

1. The error is caught.
2. The transaction is rolled back.
3. The database session remains usable.
4. An appropriate API error response is returned.

# Data Persistence

The application uses MySQL for persistent storage.

Data remains available after restarting the FastAPI application.

For example:

1. Create an employee.
2. Create a work item.
3. Stop the FastAPI server.
4. Start the FastAPI server again.
5. Request the employee or work item.
6. The previously stored data is still available.

# Swagger UI

FastAPI automatically provides Swagger UI for testing the APIs.

Swagger UI can be opened at:

```text
http://127.0.0.1:8000/docs
```

Swagger was used to test:

- Employee CRUD
- Employee search
- Employee filtering
- Employee pagination
- Work item CRUD
- Work item assignment
- Work item search
- Work item filtering
- Combined filters
- Pagination
- Validation errors
- 404 errors
- Delete operations

# What I Learned

I learned how to connect a FastAPI application to a MySQL database using SQLAlchemy.

I learned how to:

- Build REST APIs using FastAPI.
- Use Pydantic for request validation.
- Connect FastAPI to MySQL.
- Use SQLAlchemy ORM.
- Use Git branches.
- Push code to GitHub.
- Document the project using README.md.

In Task 3, I learned how to implement search, filtering and pagination using SQLAlchemy queries. I also learned how query parameters work in FastAPI and how to validate values such as limit, offset and work mode.

In Task 4, I learned how to create a WorkItem model and connect it with the Employee model using a foreign key and SQLAlchemy relationship. I also learned how to implement work item CRUD operations, filtering, combined filters, pagination, validation and assigned employee details in API responses.

# Difficulties

I faced difficulties while setting up the MySQL connection, configuring the database connection details, handling duplicate email validation, and understanding SQLAlchemy database operations.

I also faced some issues while testing the APIs using Swagger UI.

During Task 3, I faced difficulties while implementing the pagination response structure, combining multiple filters, and testing different query parameter combinations.

During Task 4, I faced difficulties while implementing the Employee and WorkItem relationship, handling the assigned employee response, testing combined filters and pagination, and validating invalid status, priority and employee values.

# Project Status

## Task 1

Employee Management API implemented.

## Task 2

MySQL database integration and SQLAlchemy persistence implemented.

## Task 3

Employee search, filtering and pagination implemented.

## Task 4

Work Item Management API implemented with:

- Work item CRUD
- Employee assignment
- Employee reassignment
- Foreign key relationship
- SQLAlchemy relationship
- Work item search
- Work item filtering
- Combined filters
- Pagination
- Validation
- Error handling
- Database persistence

# Conclusion

This project demonstrates a FastAPI backend connected to MySQL using SQLAlchemy.

The application supports employee management and work item management with validation, CRUD operations, search, filtering, pagination, database relationships and persistent storage.

The project was tested using Swagger UI and the code is maintained using Git and GitHub.
