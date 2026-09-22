from fastapi import Depends, FastAPI, HTTPException, Path, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from . import models  # noqa: F401
from .database import Base, engine, get_db
from .schemas import EmployeeCreate, EmployeeResponse, EmployeeUpdate
from .services import (
    DuplicateEmailError,
    EmployeeNotFoundError,
    create_employee,
    delete_employee,
    get_all_employees,
    get_employee,
    update_employee,
)


app = FastAPI(
    title="Employee Management API",
    description="Employee Management API using FastAPI, MySQL and SQLAlchemy",
    version="2.0.0",
)


@app.on_event("startup")
def startup() -> None:
    try:
        Base.metadata.create_all(bind=engine)
    except SQLAlchemyError as exc:
        # Keep the API running, but show the real database problem
        # in the terminal for debugging.
        print(f"DATABASE STARTUP ERROR: {exc}")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    errors = []

    for error in exc.errors():
        field = ".".join(str(item) for item in error["loc"])
        message = error["msg"]

        errors.append(
            {
                "field": field,
                "message": message,
            }
        )

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error.",
            "errors": errors,
        },
    )


@app.exception_handler(SQLAlchemyError)
async def sqlalchemy_exception_handler(
    request: Request,
    exc: SQLAlchemyError,
) -> JSONResponse:
    # Print the actual database error in the Uvicorn terminal.
    # Do not expose database credentials/details to API users.
    print(f"DATABASE ERROR: {exc}")

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Database operation failed. Please check the MySQL connection and try again."
        },
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
        "message": "Application is running",
    }


@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee_api(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_employee(db, employee)

    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@app.get(
    "/employees",
    response_model=list[EmployeeResponse],
)
def get_employees(
    db: Session = Depends(get_db),
):
    return get_all_employees(db)


@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
)
def get_employee_by_id(
    employee_id: int = Path(
        ...,
        description="Employee ID must be greater than 0",
    ),
    db: Session = Depends(get_db),
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than 0.",
        )

    try:
        return get_employee(db, employee_id)

    except EmployeeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc


@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse,
)
def update_employee_api(
    employee: EmployeeUpdate,
    employee_id: int = Path(
        ...,
        description="Employee ID must be greater than 0",
    ),
    db: Session = Depends(get_db),
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than 0.",
        )

    try:
        return update_employee(
            db,
            employee_id,
            employee,
        )

    except EmployeeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc

    except DuplicateEmailError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(exc),
        ) from exc


@app.delete("/employees/{employee_id}")
def delete_employee_api(
    employee_id: int = Path(
        ...,
        description="Employee ID must be greater than 0",
    ),
    db: Session = Depends(get_db),
):
    if employee_id <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Employee ID must be greater than 0.",
        )

    try:
        delete_employee(db, employee_id)

        return {
            "message": "Employee deleted successfully."
        }

    except EmployeeNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        ) from exc