from fastapi import FastAPI, HTTPException, Path

from app.schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from app.services import (
    create_employee,
    get_all_employees,
    get_employee,
    update_employee,
    delete_employee,
)

app = FastAPI(
    title="Employee Management API",
    description="FastAPI backend for managing employee records",
    version="1.0.0",
)


@app.get("/")
def home():
    return {"message": "Employee Management API is running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/employees", response_model=EmployeeResponse, status_code=201)
def add_employee(employee: EmployeeCreate):
    # Required text fields must not be empty/whitespace-only.
    required_fields = {
        "name": employee.name,
        "department": employee.department,
        "primary_skill": employee.primary_skill,
        "location": employee.location,
    }

    for field, value in required_fields.items():
        if not value.strip():
            raise HTTPException(
                status_code=422,
                detail=f"{field} must not be empty"
            )

    # Email must be unique (case-insensitive).
    email = str(employee.email).lower()
    if any(str(item["email"]).lower() == email for item in get_all_employees()):
        raise HTTPException(
            status_code=409,
            detail="Email already exists"
        )

    return create_employee(employee)


@app.get("/employees", response_model=list[EmployeeResponse])
def read_employees():
    return get_all_employees()


@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
def read_employee(
    employee_id: int = Path(..., gt=0, description="Employee ID must be greater than 0")
):
    employee = get_employee(employee_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


@app.put("/employees/{employee_id}", response_model=EmployeeResponse)
def edit_employee(
    employee_id: int,
    employee: EmployeeUpdate,
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="Employee ID must be greater than 0"
        )

    existing = get_employee(employee_id)

    if existing is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    update_data = employee.model_dump(exclude_unset=True)

    for field in ("name", "department", "primary_skill", "location"):
        if field in update_data and (
            not isinstance(update_data[field], str)
            or not update_data[field].strip()
        ):
            raise HTTPException(
                status_code=422,
                detail=f"{field} must not be empty"
            )

    if "email" in update_data:
        email = str(update_data["email"]).lower()
        if any(
            item["id"] != employee_id
            and str(item["email"]).lower() == email
            for item in get_all_employees()
        ):
            raise HTTPException(
                status_code=409,
                detail="Email already exists"
            )

    return update_employee(employee_id, employee)


@app.delete("/employees/{employee_id}")
def remove_employee(employee_id: int):
    if employee_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="Employee ID must be greater than 0"
        )

    deleted_employee = delete_employee(employee_id)

    if deleted_employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")

    return {
        "message": "Employee deleted successfully",
        "employee": deleted_employee,
    }
