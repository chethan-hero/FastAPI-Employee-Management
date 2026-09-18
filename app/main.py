from fastapi import FastAPI, HTTPException, Path, status
from typing import List

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
    description="FastAPI Employee Management System - Task 1",
    version="1.0.0",
)


@app.get("/")
def home():
    return {
        "message": "Employee Management API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "message": "Application is running"
    }


@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def add_employee(employee: EmployeeCreate):
    try:
        return create_employee(employee)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@app.get(
    "/employees",
    response_model=List[EmployeeResponse]
)
def list_employees():
    return get_all_employees()


@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee_by_id(
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID must be greater than 0"
    )
):
    employee = get_employee(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    return employee


@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def edit_employee(
    employee: EmployeeUpdate,
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID must be greater than 0"
    )
):
    try:
        updated_employee = update_employee(employee_id, employee)

        if updated_employee is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Employee not found"
            )

        return updated_employee

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@app.delete("/employees/{employee_id}")
def remove_employee(
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID must be greater than 0"
    )
):
    deleted = delete_employee(employee_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully"
    }
