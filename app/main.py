from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query, Response, status
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session, joinedload

from app.database import Base, engine, get_db
from app.models import Employee, WorkItem
from app import schemas, services

VALID_WORK_MODES = {"WFH", "WFO"}
VALID_STATUSES = {"TODO", "IN_PROGRESS", "COMPLETED"}
VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH"}


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="Employee Management API",
    description="Employee and Work Item Management System",
    version="5.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "message": "Application is running",
    }


@app.post(
    "/employees",
    response_model=schemas.EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
):
    try:
        existing = (
            db.query(Employee)
            .filter(func.lower(Employee.email) == employee.email.lower())
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=400,
                detail="Email already exists",
            )

        new_employee = Employee(
            **employee.model_dump()
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
            detail="Database constraint error",
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error",
        )

@app.get(
    "/employees",
    response_model=schemas.EmployeeListResponse,
)
def get_employees(
    search: str | None = None,
    department: str | None = None,
    work_mode: str | None = None,
    is_active: bool | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    try:
        query = db.query(Employee)

        if search:
            query = query.filter(Employee.name.ilike(f"%{search}%"))

        if department:
            query = query.filter(Employee.department == department)

        if work_mode:
            work_mode = work_mode.upper()

            if work_mode not in VALID_WORK_MODES:
                raise HTTPException(
                    status_code=422,
                    detail="work_mode must be WFH or WFO",
                )

            query = query.filter(Employee.work_mode == work_mode)

        if is_active is not None:
            query = query.filter(Employee.is_active == is_active)

        total = query.count()

        items = (
            query.order_by(Employee.id.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": items,
        }

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error",
        )
@app.get(
    "/employees/{employee_id}",
    response_model=schemas.EmployeeResponse,
)
def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return employee


@app.put(
    "/employees/{employee_id}",
    response_model=schemas.EmployeeResponse,
)
def update_employee(
    employee_id: int,
    employee: schemas.EmployeeUpdate,
    db: Session = Depends(get_db),
):
    existing = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if existing is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    try:
        update_data = employee.model_dump(exclude_unset=True)

        if "email" in update_data:
            duplicate = (
                db.query(Employee)
                .filter(
                    func.lower(Employee.email)
                    == update_data["email"].lower(),
                    Employee.id != employee_id,
                )
                .first()
            )

            if duplicate:
                raise HTTPException(
                    status_code=400,
                    detail="Email already exists",
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
            detail="Database constraint error",
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error",
        )

@app.delete(
    "/employees/{employee_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    try:
        db.delete(employee)
        db.commit()
        return Response(status_code=204)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error",
        )

@app.post(
    "/work-items",
    response_model=schemas.WorkItemResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_work_item(
    work_item: schemas.WorkItemCreate,
    db: Session = Depends(get_db),
):
    employee = (
        db.query(Employee)
        .filter(Employee.id == work_item.employee_id)
        .first()
    )

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Assigned employee not found",
        )

    try:
        new_work_item = WorkItem(**work_item.model_dump())

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
            detail="Database constraint error",
        )

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error",
        )


@app.get(
    "/work-items",
    response_model=schemas.WorkItemListResponse,
)
def get_work_items(
    search: str | None = None,
    employee_id: int | None = Query(default=None, gt=0),
    status_filter: str | None = Query(default=None, alias="status"),
    priority: str | None = None,
    limit: int = Query(default=10, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
):
    try:
        query = (
            db.query(WorkItem)
            .options(joinedload(WorkItem.assigned_employee))
        )

        if search:
            query = query.filter(WorkItem.title.ilike(f"%{search}%"))

        if employee_id is not None:
            query = query.filter(WorkItem.employee_id == employee_id)

        if status_filter:
            status_filter = status_filter.upper()

            if status_filter not in VALID_STATUSES:
                raise HTTPException(
                    status_code=422,
                    detail="status must be TODO, IN_PROGRESS or COMPLETED",
                )

            query = query.filter(WorkItem.status == status_filter)

        if priority:
            priority = priority.upper()

            if priority not in VALID_PRIORITIES:
                raise HTTPException(
                    status_code=422,
                    detail="priority must be LOW, MEDIUM or HIGH",
                )

            query = query.filter(WorkItem.priority == priority)

        total = query.count()

        items = (
            query.order_by(WorkItem.id.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return {
            "total": total,
            "limit": limit,
            "offset": offset,
            "items": items,
        }

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error",
        )


@app.get(
    "/work-items/{work_item_id}",
    response_model=schemas.WorkItemResponse,
)
def get_work_item(
    work_item_id: int,
    db: Session = Depends(get_db),
):
    try:
        work_item = (
            db.query(WorkItem)
            .options(joinedload(WorkItem.assigned_employee))
            .filter(WorkItem.id == work_item_id)
            .first()
        )

        if work_item is None:
            raise HTTPException(
                status_code=404,
                detail="Work item not found",
            )

        return work_item

    except HTTPException:
        raise

    except SQLAlchemyError:
        raise HTTPException(
            status_code=500,
            detail="Database error",
        )


@app.get(
    "/employees/{employee_id}/work-items/summary",
    response_model=schemas.EmployeeWorkItemSummary,
)
def employee_work_item_summary(
    employee_id: int,
    db: Session = Depends(get_db),
):
    summary = services.get_employee_work_item_summary(
        db=db,
        employee_id=employee_id,
    )

    if summary is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found",
        )

    return summary

@app.put(
    "/work-items/{work_item_id}",
    response_model=schemas.WorkItemResponse,
)
def update_work_item_put(
    work_item_id: int,
    payload: schemas.WorkItemUpdate,
    db: Session = Depends(get_db),
):
    try:
        work_item = services.update_work_item(
            db,
            work_item_id,
            payload.model_dump(exclude_unset=True),
        )

    except services.StatusTransitionError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found",
        )

    return work_item


@app.patch(
    "/work-items/{work_item_id}",
    response_model=schemas.WorkItemResponse,
)
def update_work_item_patch(
    work_item_id: int,
    payload: schemas.WorkItemUpdate,
    db: Session = Depends(get_db),
):
    try:
        work_item = services.update_work_item(
            db,
            work_item_id,
            payload.model_dump(exclude_unset=True),
        )

    except services.StatusTransitionError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found",
        )

    return work_item


@app.delete(
    "/work-items/{work_item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_work_item(
    work_item_id: int,
    db: Session = Depends(get_db),
):
    work_item = (
        db.query(WorkItem)
        .filter(WorkItem.id == work_item_id)
        .first()
    )

    if work_item is None:
        raise HTTPException(
            status_code=404,
            detail="Work item not found",
        )

    try:
        db.delete(work_item)
        db.commit()
        return Response(status_code=204)

    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Database error",
        )