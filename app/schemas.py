from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: str = "WFO"
    is_active: bool = True

    @field_validator(
        "name",
        "department",
        "primary_skill",
        "location"
    )
    @classmethod
    def validate_required_strings(cls, value: str):
        if not value.strip():
            raise ValueError("Field must not be blank")
        return value.strip()

    @field_validator("work_mode")
    @classmethod
    def validate_work_mode(cls, value: str):
        value = value.strip().upper()

        if value not in {"WFH", "WFO"}:
            raise ValueError("work_mode must be WFH or WFO")

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
        "email",
        "department",
        "primary_skill",
        "location",
        "work_mode"
    )
    @classmethod
    def validate_update_strings(cls, value):
        if value is None:
            return value

        if isinstance(value, str) and not value.strip():
            raise ValueError("Field must not be blank")

        return value.strip() if isinstance(value, str) else value

    @field_validator("work_mode")
    @classmethod
    def validate_update_work_mode(cls, value):
        if value is None:
            return value

        value = value.upper()

        if value not in {"WFH", "WFO"}:
            raise ValueError("work_mode must be WFH or WFO")

        return value


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class EmployeeListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[EmployeeResponse]


class AssignedEmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)


class WorkItemCreate(BaseModel):
    title: str
    description: Optional[str] = None
    employee_id: int = Field(..., gt=0)
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str):
        if not value.strip():
            raise ValueError("title must not be blank")

        return value.strip()

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        if value is None:
            return None

        return value.strip()

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str):
        value = value.strip().upper()

        if value not in {"TODO", "IN_PROGRESS", "COMPLETED"}:
            raise ValueError(
                "status must be TODO, IN_PROGRESS or COMPLETED"
            )

        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value: str):
        value = value.strip().upper()

        if value not in {"LOW", "MEDIUM", "HIGH"}:
            raise ValueError(
                "priority must be LOW, MEDIUM or HIGH"
            )

        return value


class WorkItemUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    employee_id: Optional[int] = Field(default=None, gt=0)
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title")
    @classmethod
    def validate_update_title(cls, value):
        if value is None:
            return None

        if not value.strip():
            raise ValueError("title must not be blank")

        return value.strip()

    @field_validator("description")
    @classmethod
    def validate_update_description(cls, value):
        if value is None:
            return None

        return value.strip()

    @field_validator("status")
    @classmethod
    def validate_update_status(cls, value):
        if value is None:
            return None

        value = value.strip().upper()

        if value not in {"TODO", "IN_PROGRESS", "COMPLETED"}:
            raise ValueError(
                "status must be TODO, IN_PROGRESS or COMPLETED"
            )

        return value

    @field_validator("priority")
    @classmethod
    def validate_update_priority(cls, value):
        if value is None:
            return None

        value = value.strip().upper()

        if value not in {"LOW", "MEDIUM", "HIGH"}:
            raise ValueError(
                "priority must be LOW, MEDIUM or HIGH"
            )

        return value


class WorkItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    employee_id: int
    status: str
    priority: str
    due_date: Optional[date]
    created_at: datetime
    assigned_employee: AssignedEmployeeResponse

    model_config = ConfigDict(from_attributes=True)


class WorkItemListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: list[WorkItemResponse]