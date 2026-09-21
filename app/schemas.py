from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, EmailStr, field_validator


class EmployeeBase(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: Literal["WFH", "WFO"]

    @field_validator(
        "name",
        "department",
        "primary_skill",
        "location"
    )
    @classmethod
    def validate_required_fields(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError(
                "Field cannot be empty or whitespace-only"
            )
        return value

    @field_validator("email")
    @classmethod
    def normalize_email(cls, value: EmailStr) -> str:
        return str(value).strip().lower()
class EmployeeCreate(EmployeeBase):
    pass
class EmployeeUpdate(EmployeeBase):
    pass
class EmployeeResponse(EmployeeBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )