from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


VALID_WORK_MODES = {"WFH", "WFO"}
VALID_STATUSES = {"TODO", "IN_PROGRESS", "COMPLETED"}
VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH"}


def validate_required_text(value: str) -> str:
    value = value.strip()

    if not value:
        raise ValueError("This field cannot be empty or contain only spaces.")

    return value


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: str
    is_active: bool = True

    @field_validator(
        "name",
        "department",
        "primary_skill",
        "location",
        mode="before",
    )
    @classmethod
    def validate_text_fields(cls, value):
        if not isinstance(value, str):
            raise ValueError("Value must be a string.")

        return validate_required_text(value)

    @field_validator("work_mode")
    @classmethod
    def validate_work_mode(cls, value):
        value = value.strip().upper()

        if value not in VALID_WORK_MODES:
            raise ValueError("work_mode must be either WFH or WFO.")

        return value


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    primary_skill: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = None
    is_active: Optional[bool] = None

    @field_validator(
        "name",
        "department",
        "primary_skill",
        "location",
        mode="before",
    )
    @classmethod
    def validate_text_fields(cls, value):
        if value is None:
            return value

        if not isinstance(value, str):
            raise ValueError("Value must be a string.")

        return validate_required_text(value)

    @field_validator("work_mode")
    @classmethod
    def validate_work_mode(cls, value):
        if value is None:
            return value

        value = value.strip().upper()

        if value not in VALID_WORK_MODES:
            raise ValueError("work_mode must be either WFH or WFO.")

        return value


class EmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: str
    is_active: bool
    created_at: datetime


class EmployeeListResponse(BaseModel):
    items: list[EmployeeResponse]
    total: int
    limit: int
    offset: int



class WorkItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    employee_id: int
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: Optional[date] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value):
        if not isinstance(value, str):
            raise ValueError("Title must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty or contain only spaces.")

        return value

    @field_validator("description", mode="before")
    @classmethod
    def validate_description(cls, value):
        if value is None:
            return value

        if not isinstance(value, str):
            raise ValueError("Description must be a string.")

        return value.strip()

    @field_validator("employee_id")
    @classmethod
    def validate_employee_id(cls, value):
        if value <= 0:
            raise ValueError("employee_id must be greater than 0.")

        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        value = value.strip().upper()

        if value not in VALID_STATUSES:
            raise ValueError(
                "status must be TODO, IN_PROGRESS or COMPLETED."
            )

        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):
        value = value.strip().upper()

        if value not in VALID_PRIORITIES:
            raise ValueError(
                "priority must be LOW, MEDIUM or HIGH."
            )

        return value


class WorkItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    employee_id: Optional[int] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            return value

        if not isinstance(value, str):
            raise ValueError("Title must be a string.")

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty or contain only spaces.")

        return value

    @field_validator("description", mode="before")
    @classmethod
    def validate_description(cls, value):
        if value is None:
            return value

        if not isinstance(value, str):
            raise ValueError("Description must be a string.")

        return value.strip()

    @field_validator("employee_id")
    @classmethod
    def validate_employee_id(cls, value):
        if value is None:
            return value

        if value <= 0:
            raise ValueError("employee_id must be greater than 0.")

        return value

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value is None:
            return value

        value = value.strip().upper()

        if value not in VALID_STATUSES:
            raise ValueError(
                "status must be TODO, IN_PROGRESS or COMPLETED."
            )

        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):
        if value is None:
            return value

        value = value.strip().upper()

        if value not in VALID_PRIORITIES:
            raise ValueError(
                "priority must be LOW, MEDIUM or HIGH."
            )

        return value

class AssignedEmployeeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    email: EmailStr


class WorkItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    title: str
    description: Optional[str]
    employee_id: int
    status: str
    priority: str
    due_date: Optional[date]
    created_at: datetime
    assigned_employee: AssignedEmployeeResponse

class WorkItemListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[WorkItemResponse]