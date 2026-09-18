from fastapi import FastAPI, HTTPException, Path, status

from .schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from .services import (
    create_employee,
    delete_employee,
    email_exists,
    get_all_employees,
    get_employee_by_id,
    update_employee,
)


app = FastAPI(
    title="Employee Management API",
    description="Beginner FastAPI application for managing employee records",
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "success",
        "message": "Employee Management API is running"
    }


@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_new_employee(employee: EmployeeCreate):

    if email_exists(str(employee.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    return create_employee(employee)


@app.get(
    "/employees",
    response_model=list[EmployeeResponse],
)
def list_employees():
    return get_all_employees()


@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
)
def get_employee(
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID must be greater than 0"
    )
):
    employee = get_employee_by_id(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )

    return employee


@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
)
def update_existing_employee(
    employee: EmployeeUpdate,
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID must be greater than 0"
    )
):

    existing_employee = get_employee_by_id(employee_id)

    if existing_employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )

    if email_exists(str(employee.email), exclude_id=employee_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )

    return update_employee(employee_id, employee)


@app.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_200_OK,
)
def delete_existing_employee(
    employee_id: int = Path(
        ...,
        gt=0,
        description="Employee ID must be greater than 0"
    )
):

    employee = delete_employee(employee_id)

    if employee is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Employee with ID {employee_id} not found"
        )

    return {
        "message": f"Employee with ID {employee_id} deleted successfully",
        "employee": employee
    }