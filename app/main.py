from fastapi import (
    FastAPI,
    Depends,
    HTTPException,
    Query,
    status
)

from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    EmployeeCreate,
    EmployeeUpdate,
    EmployeeResponse,
    EmployeeListResponse
)

from app.services import (
    create_employee,
    get_employees,
    get_employee_by_id,
    update_employee,
    delete_employee
)


app = FastAPI(
    title="Employee Management API",
    description="FastAPI Employee Management API using MySQL and SQLAlchemy",
    version="3.0.0"
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
def create_employee_api(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    new_employee, error = create_employee(
        db,
        employee
    )

    if error:
        if "Email already exists" in error:
            raise HTTPException(
                status_code=409,
                detail=error
            )

        raise HTTPException(
            status_code=500,
            detail=error
        )

    return new_employee

@app.get(
    "/employees",
    response_model=EmployeeListResponse
)
def list_employees(
    search: str | None = Query(
        default=None,
        description="Search employee name using partial, case-insensitive matching"
    ),

    department: str | None = Query(
        default=None,
        description="Filter employees by department"
    ),

    work_mode: str | None = Query(
        default=None,
        description="Filter by work mode: WFH or WFO"
    ),

    is_active: bool | None = Query(
        default=None,
        description="Filter by active status: true or false"
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100,
        description="Maximum number of employees to return (1-100)"
    ),

    offset: int = Query(
        default=0,
        ge=0,
        description="Number of matching employees to skip"
    ),

    db: Session = Depends(get_db)
):
    # Validate work mode
    if work_mode is not None:
        work_mode = work_mode.strip().upper()

        if work_mode not in ["WFH", "WFO"]:
            raise HTTPException(
                status_code=422,
                detail="work_mode must be either WFH or WFO"
            )

    total, employees, error = get_employees(
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
    response_model=EmployeeResponse
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

    employee, error = get_employee_by_id(
        db,
        employee_id
    )

    if error:
        raise HTTPException(
            status_code=500,
            detail=error
        )

    if employee is None:
        raise HTTPException(
            status_code=404,
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
            status_code=422,
            detail="Employee ID must be greater than 0"
        )

    updated_employee, error = update_employee(
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

        if "Email already exists" in error:
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
def delete_employee_api(
    employee_id: int,
    db: Session = Depends(get_db)
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=422,
            detail="Employee ID must be greater than 0"
        )

    deleted_employee, error = delete_employee(
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
        "id": employee_id
    }