from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate


def create_employee(
    db: Session,
    employee_data: EmployeeCreate
):
    try:
        # Case-insensitive email duplicate check
        existing_employee = (
            db.query(Employee)
            .filter(
                func.lower(Employee.email)
                == employee_data.email.lower()
            )
            .first()
        )

        if existing_employee:
            return None, "Email already exists"

        employee = Employee(
            name=employee_data.name,
            email=employee_data.email,
            department=employee_data.department,
            primary_skill=employee_data.primary_skill,
            location=employee_data.location,
            work_mode=employee_data.work_mode,
            is_active=employee_data.is_active
        )

        db.add(employee)
        db.commit()
        db.refresh(employee)

        return employee, None

    except IntegrityError:
        db.rollback()
        return None, "Email already exists"

    except SQLAlchemyError as exc:
        db.rollback()
        return None, f"Database error: {str(exc)}"


def get_employees(
    db: Session,
    search: str | None = None,
    department: str | None = None,
    work_mode: str | None = None,
    is_active: bool | None = None,
    limit: int = 10,
    offset: int = 0
):
    try:
        # Start SQLAlchemy query
        query = db.query(Employee)

        # Search employee name - case insensitive partial match
        if search:
            search = search.strip()

            if search:
                query = query.filter(
                    Employee.name.ilike(f"%{search}%")
                )

        # Department filter
        if department:
            query = query.filter(
                Employee.department == department.strip()
            )

        # Work mode filter
        if work_mode:
            query = query.filter(
                Employee.work_mode == work_mode
            )

        # Active/inactive filter
        if is_active is not None:
            query = query.filter(
                Employee.is_active == is_active
            )

        # Count matching records BEFORE pagination
        total = query.count()

        # Sort by employee ID ascending
        employees = (
            query
            .order_by(Employee.id.asc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return total, employees, None

    except SQLAlchemyError as exc:
        return 0, [], f"Database error: {str(exc)}"


def get_employee_by_id(
    db: Session,
    employee_id: int
):
    try:
        return (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        ), None

    except SQLAlchemyError as exc:
        return None, f"Database error: {str(exc)}"


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate
):
    try:
        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if employee is None:
            return None, "Employee not found"

        update_data = employee_data.model_dump(
            exclude_unset=True
        )

        # Case-insensitive email duplicate check
        if "email" in update_data:
            existing_employee = (
                db.query(Employee)
                .filter(
                    func.lower(Employee.email)
                    == update_data["email"].lower(),
                    Employee.id != employee_id
                )
                .first()
            )

            if existing_employee:
                return None, "Email already exists"

        # Update only supplied fields
        for field, value in update_data.items():
            setattr(employee, field, value)

        # created_at is intentionally NOT changed
        db.commit()
        db.refresh(employee)

        return employee, None

    except IntegrityError:
        db.rollback()
        return None, "Email already exists"

    except SQLAlchemyError as exc:
        db.rollback()
        return None, f"Database error: {str(exc)}"


def delete_employee(
    db: Session,
    employee_id: int
):
    try:
        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if employee is None:
            return None, "Employee not found"

        db.delete(employee)
        db.commit()

        return employee, None

    except SQLAlchemyError as exc:
        db.rollback()
        return None, f"Database error: {str(exc)}"