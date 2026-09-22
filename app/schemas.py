from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


WorkMode = Literal["WFH", "WFO"]


def validate_required_text(value: str) -> str:
    value = value.strip()
    if not value:
        raise ValueError("This field cannot be empty or contain only spaces.")
    return value


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    department: str = Field(min_length=1)
    primary_skill: str = Field(min_length=1)
    location: str = Field(min_length=1)
    work_mode: WorkMode

    @field_validator("name", "department", "primary_skill", "location")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        return validate_required_text(value)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Chethan",
                "email": "chethan@gmail.com",
                "department": "Development",
                "primary_skill": "Python",
                "location": "Mandya",
                "work_mode": "WFO",
            }
        }
    )


class EmployeeUpdate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    department: str = Field(min_length=1)
    primary_skill: str = Field(min_length=1)
    location: str = Field(min_length=1)
    work_mode: WorkMode
    is_active: bool

    @field_validator("name", "department", "primary_skill", "location")
    @classmethod
    def validate_text_fields(cls, value: str) -> str:
        return validate_required_text(value)

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Chethan Updated",
                "email": "chethan@gmail.com",
                "department": "Development",
                "primary_skill": "Python",
                "location": "Mandya",
                "work_mode": "WFO",
                "is_active": False,
            }
        }
    )


class EmployeeResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: WorkMode
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
