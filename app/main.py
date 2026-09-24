from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import Base, engine, get_db
from app import models
from app import schemas
from app import services


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables automatically on application startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Employee Management API",
    description="FastAPI Employee Management System",
    version="3.0.0",
    lifespan=lifespan
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
    response_model=schemas.EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    created_employee, error = services.create_employee(db, employee)

    if error:
        if error == "Email already exists":
            raise HTTPException(
                status_code=409,
                detail=error
            )

        raise HTTPException(
            status_code=500,
            detail=error
        )

    return created_employee


@app.get(
    "/employees",
    response_model=schemas.EmployeeListResponse
)
def get_employees(
    search: str | None = Query(None),
    department: str | None = Query(None),
    work_mode: str | None = Query(None),
    is_active: bool | None = Query(None),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    if work_mode is not None:
        work_mode = work_mode.strip().upper()

        if work_mode not in ["WFH", "WFO"]:
            raise HTTPException(
                status_code=422,
                detail="work_mode must be either WFH or WFO"
            )

    total, employees, error = services.get_employees(
        db=db,
        search=search,
        department=department,
        work_mode=work_mode,
        is_active=is_active,
        limit=limit,
        offset=offset
    )

    if error:
        raise HTTPException(
            status_code=500,
            detail=error
        )

    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "items": employees
    }


@app.get(
    "/employees/{employee_id}",
    response_model=schemas.EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="Employee ID must be greater than 0"
        )

    employee, error = services.get_employee_by_id(
        db,
        employee_id
    )

    if error:
        if error == "Employee not found":
            raise HTTPException(
                status_code=404,
                detail=error
            )

        raise HTTPException(
            status_code=500,
            detail=error
        )

    return employee


@app.put(
    "/employees/{employee_id}",
    response_model=schemas.EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db)
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="Employee ID must be greater than 0"
        )

    updated_employee, error = services.update_employee(
        db,
        employee_id,
        employee
    )

    if error:
        if error == "Employee not found":
            raise HTTPException(
                status_code=404,
                detail=error
            )

        if error == "Email already exists":
            raise HTTPException(
                status_code=409,
                detail=error
            )

        raise HTTPException(
            status_code=500,
            detail=error
        )

    return updated_employee


@app.delete("/employees/{employee_id}")
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="Employee ID must be greater than 0"
        )

    deleted_employee, error = services.delete_employee(
        db,
        employee_id
    )

    if error:
        if error == "Employee not found":
            raise HTTPException(
                status_code=404,
                detail=error
            )

        raise HTTPException(
            status_code=500,
            detail=error
        )

    return {
        "message": "Employee deleted successfully",
        "employee": deleted_employee
    }