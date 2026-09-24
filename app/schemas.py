from datetime import datetime
from typing import Optional, List

from pydantic import (
    BaseModel,
    EmailStr,
    field_validator,
    model_validator
)


class EmployeeBase(BaseModel):
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
        "location"
    )
    @classmethod
    def validate_required_text(cls, value: str):
        if not value.strip():
            raise ValueError(
                "This field cannot be empty or contain only spaces"
            )
        return value.strip()

    @field_validator("work_mode")
    @classmethod
    def validate_work_mode(cls, value: str):
        value = value.strip().upper()

        if value not in ["WFH", "WFO"]:
            raise ValueError(
                "work_mode must be either WFH or WFO"
            )

        return value


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    primary_skill: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[str] = None
    is_active: Optional[bool] = None

    @model_validator(mode="before")
    @classmethod
    def reject_null_values(cls, data):
        if isinstance(data, dict):
            for field, value in data.items():
                if value is None:
                    raise ValueError(
                        f"{field} cannot be null"
                    )

        return data

    @field_validator(
        "name",
        "department",
        "primary_skill",
        "location"
    )
    @classmethod
    def validate_optional_text(cls, value):
        if value is not None:
            if not value.strip():
                raise ValueError(
                    "This field cannot be empty or contain only spaces"
                )
            return value.strip()

        return value

    @field_validator("work_mode")
    @classmethod
    def validate_optional_work_mode(cls, value):
        if value is not None:
            value = value.strip().upper()

            if value not in ["WFH", "WFO"]:
                raise ValueError(
                    "work_mode must be either WFH or WFO"
                )

            return value

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

    class Config:
        from_attributes = True


class EmployeeListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    items: List[EmployeeResponse]