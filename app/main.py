from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.database import Base, engine, get_db
from app.models import Employee, WorkItem
from app.schemas import (
    EmployeeCreate,
    EmployeeListResponse,
    EmployeeResponse,
    EmployeeUpdate,
    WorkItemCreate,
    WorkItemListResponse,
    WorkItemResponse,
    WorkItemUpdate,
    
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Employee Management API",
    description="Employee and Work Item Management System",
    version="4.0.0",
    lifespan=lifespan
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "Application is running"
    }


@app.post(
    "/employees",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED
)
def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    try:
        existing_employee = (
            db.query(Employee)
            .filter(func.lower(Employee.email) == employee.email.lower())
            .first()
        )

        if existing_employee:
            raise HTTPException(
                status_code=400,
                detail="Email already exists"
            )

        new_employee = Employee(
            name=employee.name,
            email=employee.email,
            department=employee.department,
            primary_skill=employee.primary_skill,
            location=employee.location,
            work_mode=employee.work_mode,
            is_active=employee.is_active
        )

        db.add(new_employee)
        db.commit()
        db.refresh(new_employee)

        return new_employee

    except HTTPException:
        db.rollback()
        raise

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Database constraint error"
        )

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@app.get(
    "/employees",
    response_model=EmployeeListResponse
)
def get_employees(
    search: str | None = None,
    department: str | None = None,
    work_mode: str | None = None,
    is_active: bool | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    try:
        query = db.query(Employee)

        if search:
            query = query.filter(
                Employee.name.ilike(f"%{search}%")
            )

        if department:
            query = query.filter(
                Employee.department == department
            )

        if work_mode:
            work_mode = work_mode.upper()

            if work_mode not in {"WFH", "WFO"}:
                raise HTTPException(
                    status_code=422,
                    detail="work_mode must be WFH or WFO"
                )

            query = query.filter(
                Employee.work_mode == work_mode
            )

        if is_active is not None:
            query = query.filter(
                Employee.is_active == is_active
            )

        total = query.count()

        employees = (
            query
            .order_by(Employee.id.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": employees
        }

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@app.get(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return employee


@app.put(
    "/employees/{employee_id}",
    response_model=EmployeeResponse
)
def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    try:
        update_data = employee.model_dump(
            exclude_unset=True
        )

        if "email" in update_data:
            duplicate = (
                db.query(Employee)
                .filter(
                    func.lower(Employee.email)
                    == update_data["email"].lower(),
                    Employee.id != employee_id
                )
                .first()
            )

            if duplicate:
                raise HTTPException(
                    status_code=400,
                    detail="Email already exists"
                )

        for key, value in update_data.items():
            setattr(existing, key, value)

        db.commit()
        db.refresh(existing)

        return existing

    except HTTPException:
        db.rollback()
        raise

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Database constraint error"
        )

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@app.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    try:
        db.delete(employee)
        db.commit()

        return Response(status_code=204)

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@app.post(
    "/work-items",
    response_model=WorkItemResponse,
    status_code=status.HTTP_201_CREATED
)
def create_work_item(
    work_item: WorkItemCreate,
    db: Session = Depends(get_db)
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == work_item.employee_id)
        .first()
    )

    if not employee:
        raise HTTPException(
            status_code=404,
            detail="Assigned employee not found"
        )

    try:
        new_work_item = WorkItem(
            title=work_item.title,
            description=work_item.description,
            employee_id=work_item.employee_id,
            status=work_item.status,
            priority=work_item.priority,
            due_date=work_item.due_date
        )

        db.add(new_work_item)
        db.commit()
        db.refresh(new_work_item)

        return (
            db.query(WorkItem)
            .options(joinedload(WorkItem.assigned_employee))
            .filter(WorkItem.id == new_work_item.id)
            .first()
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Database constraint error"
        )

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@app.get(
    "/work-items",
    response_model=WorkItemListResponse
)
def get_work_items(
    search: str | None = None,
    employee_id: int | None = Query(default=None, gt=0),
    status_filter: str | None = Query(
        default=None,
        alias="status"
    ),
    priority: str | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    try:
        query = (
            db.query(WorkItem)
            .options(joinedload(WorkItem.assigned_employee))
        )

        if search:
            query = query.filter(
                WorkItem.title.ilike(f"%{search}%")
            )

        if employee_id is not None:
            query = query.filter(
                WorkItem.employee_id == employee_id
            )

        if status_filter:
            status_filter = status_filter.upper()

            if status_filter not in {
                "TODO",
                "IN_PROGRESS",
                "COMPLETED"
            }:
                raise HTTPException(
                    status_code=422,
                    detail=(
                        "status must be TODO, IN_PROGRESS "
                        "or COMPLETED"
                    )
                )

            query = query.filter(
                WorkItem.status == status_filter
            )

        if priority:
            priority = priority.upper()

            if priority not in {
                "LOW",
                "MEDIUM",
                "HIGH"
            }:
                raise HTTPException(
                    status_code=422,
                    detail=(
                        "priority must be LOW, MEDIUM or HIGH"
                    )
                )

            query = query.filter(
                WorkItem.priority == priority
            )

        total = query.count()

        items = (
            query
            .order_by(WorkItem.id.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": items
        }

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@app.get(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def get_work_item(
    work_item_id: int,
    db: Session = Depends(get_db)
):
    work_item = (
        db.query(WorkItem)
        .options(joinedload(WorkItem.assigned_employee))
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if not work_item:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    return work_item


@app.put(
    "/work-items/{work_item_id}",
    response_model=WorkItemResponse
)
def update_work_item(
    work_item_id: int,
    work_item: WorkItemUpdate,
    db: Session = Depends(get_db)
):
    existing = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if not existing:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    update_data = work_item.model_dump(
        exclude_unset=True
    )

    if "employee_id" in update_data:
        employee = (
            db.query(Employee)
            .filter(
                Employee.id == update_data["employee_id"]
            )
            .first()
        )

        if not employee:
            raise HTTPException(
                status_code=404,
                detail="Assigned employee not found"
            )

    try:
        for key, value in update_data.items():
            setattr(existing, key, value)

        db.commit()
        db.refresh(existing)

        return (
            db.query(WorkItem)
            .options(joinedload(WorkItem.assigned_employee))
            .filter(WorkItem.id == work_item_id)
            .first()
        )

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail="Database constraint error"
        )

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )


@app.delete(
    "/work-items/{work_item_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_work_item(
    work_item_id: int,
    db: Session = Depends(get_db)
):
    work_item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if not work_item:
        raise HTTPException(
            status_code=404,
            detail="Work item not found"
        )

    try:
        db.delete(work_item)
        db.commit()

        return Response(status_code=204)

    except SQLAlchemyError:
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Database error"
        )