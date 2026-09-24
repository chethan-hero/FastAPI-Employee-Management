from sqlalchemy import Column, Integer, String, Boolean, DateTime, UniqueConstraint
from datetime import datetime

from app.database import Base


class Employee(Base):
    __tablename__ = "employees"

    __table_args__ = (
        UniqueConstraint("email", name="uq_employee_email"),
    )

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)

    name = Column(String(100), nullable=False)

    email = Column(String(255), nullable=False, unique=True, index=True)

    department = Column(String(100), nullable=False)

    primary_skill = Column(String(100), nullable=False)

    location = Column(String(100), nullable=False)

    work_mode = Column(String(10), nullable=False)

    is_active = Column(Boolean, nullable=False, default=True)

    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )