from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from .models import Employee
from .schemas import EmployeeCreate, EmployeeUpdate


class EmployeeNotFoundError(Exception):
    pass


class DuplicateEmailError(Exception):
    pass


def create_employee(db: Session, employee_data: EmployeeCreate) -> Employee:
    data = employee_data.model_dump()
    data["email"] = data["email"].strip().lower()

    existing = db.scalar(
        select(Employee).where(func.lower(Employee.email) == data["email"])
    )
    if existing:
        raise DuplicateEmailError("Email address already exists.")

    employee = Employee(**data)

    try:
        db.add(employee)
        db.commit()
        db.refresh(employee)
        return employee
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateEmailError("Email address already exists.") from exc
    except SQLAlchemyError:
        db.rollback()
        raise


def get_all_employees(db: Session) -> list[Employee]:
    return list(db.scalars(select(Employee).order_by(Employee.id)).all())


def get_employee(db: Session, employee_id: int) -> Employee:
    employee = db.get(Employee, employee_id)
    if employee is None:
        raise EmployeeNotFoundError("Employee not found.")
    return employee


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate,
) -> Employee:
    employee = get_employee(db, employee_id)

    data = employee_data.model_dump()
    data["email"] = data["email"].strip().lower()

    duplicate = db.scalar(
        select(Employee).where(
            func.lower(Employee.email) == data["email"],
            Employee.id != employee_id,
        )
    )
    if duplicate:
        raise DuplicateEmailError("Email address already exists.")

    employee.name = data["name"]
    employee.email = data["email"]
    employee.department = data["department"]
    employee.primary_skill = data["primary_skill"]
    employee.location = data["location"]
    employee.work_mode = data["work_mode"]

    # Explicitly assign the boolean so false is persisted correctly.
    employee.is_active = data["is_active"]

    # created_at is intentionally not changed during an update.

    try:
        db.commit()
        db.refresh(employee)
        return employee
    except IntegrityError as exc:
        db.rollback()
        raise DuplicateEmailError("Email address already exists.") from exc
    except SQLAlchemyError:
        db.rollback()
        raise


def delete_employee(db: Session, employee_id: int) -> None:
    employee = get_employee(db, employee_id)

    try:
        db.delete(employee)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise
