from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from .models import Employee
from .schemas import EmployeeCreate, EmployeeUpdate


def create_employee(
    db: Session,
    employee_data: EmployeeCreate
):
    email = str(employee_data.email).strip().lower()

    # Case-insensitive duplicate check
    existing_employee = (
        db.query(Employee)
        .filter(func.lower(Employee.email) == email)
        .first()
    )

    if existing_employee:
        return None, "Email already exists"

    employee = Employee(
        name=employee_data.name,
        email=email,
        department=employee_data.department,
        primary_skill=employee_data.primary_skill,
        location=employee_data.location,
        work_mode=employee_data.work_mode,
        is_active=True
    )

    try:
        db.add(employee)
        db.commit()
        db.refresh(employee)

        return employee, None

    except IntegrityError:
        db.rollback()

        return None, "Email already exists"

    except Exception:
        db.rollback()
        raise


def get_all_employees(db: Session):
    return (
        db.query(Employee)
        .order_by(Employee.id)
        .all()
    )


def get_employee(
    db: Session,
    employee_id: int
):
    return (
        db.query(Employee)
        .filter(Employee.id == employee_id)
        .first()
    )


def update_employee(
    db: Session,
    employee_id: int,
    employee_data: EmployeeUpdate
):
    employee = get_employee(
        db,
        employee_id
    )

    if employee is None:
        return None, "Employee not found"

    email = str(employee_data.email).strip().lower()

    # Check email against other employees
    duplicate = (
        db.query(Employee)
        .filter(
            func.lower(Employee.email) == email,
            Employee.id != employee_id
        )
        .first()
    )

    if duplicate:
        return None, "Email already exists"

    try:
        employee.name = employee_data.name
        employee.email = email
        employee.department = employee_data.department
        employee.primary_skill = employee_data.primary_skill
        employee.location = employee_data.location
        employee.work_mode = employee_data.work_mode

        # Do NOT change:
        # employee.id
        # employee.is_active
        # employee.created_at

        db.commit()
        db.refresh(employee)

        return employee, None

    except IntegrityError:
        db.rollback()

        return None, "Email already exists"

    except Exception:
        db.rollback()
        raise


def delete_employee(
    db: Session,
    employee_id: int
):
    employee = get_employee(
        db,
        employee_id
    )

    if employee is None:
        return False

    try:
        db.delete(employee)
        db.commit()

        return True

    except Exception:
        db.rollback()
        raise