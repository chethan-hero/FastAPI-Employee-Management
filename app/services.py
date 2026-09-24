from sqlalchemy.orm import Session
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.models import Employee
from app.schemas import EmployeeCreate, EmployeeUpdate

DATABASE_ERROR = "Database error. Please try again."

def create_employee(
    db: Session,
    employee_data: EmployeeCreate
):
    try:
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
            email=employee_data.email.lower(),
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

    except SQLAlchemyError:
        db.rollback()
        return None, DATABASE_ERROR


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
        query = db.query(Employee)

        if search:
            search = search.strip()

            if search:
                query = query.filter(
                    Employee.name.ilike(f"%{search}%")
                )
        if department:
            department = department.strip()

            if department:
                query = query.filter(
                    Employee.department == department
                )

        if work_mode:
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

        return total, employees, None

    except SQLAlchemyError:
        db.rollback()
        return 0, [], DATABASE_ERROR


def get_employee_by_id(
    db: Session,
    employee_id: int
):
    try:
        employee = (
            db.query(Employee)
            .filter(Employee.id == employee_id)
            .first()
        )

        if not employee:
            return None, "Employee not found"

        return employee, None

    except SQLAlchemyError:
        db.rollback()
        return None, DATABASE_ERROR


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

        if not employee:
            return None, "Employee not found"

        update_data = employee_data.model_dump(
            exclude_unset=True
        )

        # Check duplicate email during update
        if "email" in update_data:
            new_email = update_data["email"].lower()

            existing_employee = (
                db.query(Employee)
                .filter(
                    func.lower(Employee.email) == new_email,
                    Employee.id != employee_id
                )
                .first()
            )

            if existing_employee:
                return None, "Email already exists"

            update_data["email"] = new_email

        for field, value in update_data.items():
            setattr(employee, field, value)

        db.commit()
        db.refresh(employee)

        return employee, None

    except IntegrityError:
        db.rollback()
        return None, "Email already exists"

    except SQLAlchemyError:
        db.rollback()
        return None, DATABASE_ERROR


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

        if not employee:
            return None, "Employee not found"

        db.delete(employee)
        db.commit()

        return employee, None

    except SQLAlchemyError:
        db.rollback()
        return None, DATABASE_ERROR