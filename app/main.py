from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .schemas import (
    EmployeeCreate,
    EmployeeResponse,
    EmployeeUpdate
)
from .services import (
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee,
    update_employee
)

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Employee Management API",
    description="Employee Management API using FastAPI, MySQL and SQLAlchemy",
    version="2.0.0"
)

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
def create_employee_api(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    new_employee, error = create_employee(
        db,
        employee
    )
    if error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error
        )
    return new_employee


@app.get(
    "/employees",
    response_model=list[EmployeeResponse]
)
def get_employees(
    db: Session = Depends(get_db)
):
    return get_all_employees(db)

@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee_by_id(
    employee_id: int,
    db: Session = Depends(get_db)
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than 0"
        )
    employee = get_employee(
        db,
        employee_id
    )

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
def update_employee_api(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than 0"
        )

    updated_employee, error = update_employee(
        db,
        employee_id,
        employee
    )

    if error == "Employee not found":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error
        )

    if error == "Email already exists":
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=error
        )

    return updated_employee



@app.delete("/employees/{employee_id}")
def delete_employee_api(
    employee_id: int,
    db: Session = Depends(get_db)
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than 0"
        )

    deleted = delete_employee(
        db,
        employee_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully"
    }