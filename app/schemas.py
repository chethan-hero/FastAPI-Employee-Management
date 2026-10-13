from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


VALID_STATUSES = {"TODO", "IN_PROGRESS", "COMPLETED"}
VALID_PRIORITIES = {"LOW", "MEDIUM", "HIGH"}


class WorkItemCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    employee_id: int = Field(..., gt=0)
    status: str = "TODO"
    priority: str = "MEDIUM"
    due_date: Optional[date] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title cannot be empty")
        if len(value) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        return value.strip()

    @field_validator("status")
    @classmethod
    def validate_status(cls, value):
        if value not in VALID_STATUSES:
            raise ValueError(
                "Status must be TODO, IN_PROGRESS, or COMPLETED"
            )
        return value

    @field_validator("priority")
    @classmethod
    def validate_priority(cls, value):
        if value not in VALID_PRIORITIES:
            raise ValueError(
                "Priority must be LOW, MEDIUM, or HIGH"
            )
        return value


class WorkItemUpdate(BaseModel):
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    employee_id: Optional[int] = Field(default=None, gt=0)
    status: Optional[str] = None
    priority: Optional[str] = None
    due_date: Optional[date] = None

    @field_validator("title", mode="before")
    @classmethod
    def validate_title(cls, value):
        if value is None:
            raise ValueError("Title cannot be null")
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title cannot be empty")
        if len(value) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        return value.strip()

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value):
        if value is None:
            raise ValueError("Status cannot be null")
        if value not in VALID_STATUSES:
            raise ValueError(
                "Status must be TODO, IN_PROGRESS, or COMPLETED"
            )
        return value

    @field_validator("priority", mode="before")
    @classmethod
    def validate_priority(cls, value):
        if value is None:
            raise ValueError("Priority cannot be null")
        if value not in VALID_PRIORITIES:
            raise ValueError(
                "Priority must be LOW, MEDIUM, or HIGH"
            )
        return value


class WorkItemStatusUpdate(BaseModel):
    status: str

    @field_validator("status", mode="before")
    @classmethod
    def validate_status(cls, value):
        if not isinstance(value, str) or value not in VALID_STATUSES:
            raise ValueError(
                "Status must be TODO, IN_PROGRESS, or COMPLETED"
            )
        return value


class WorkItemResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    employee_id: int
    status: str
    priority: str
    due_date: Optional[date] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class EmployeeWorkItemSummary(BaseModel):
    total_work_items: int = Field(..., ge=0)
    todo: int = Field(..., ge=0)
    in_progress: int = Field(..., ge=0)
    completed: int = Field(..., ge=0)