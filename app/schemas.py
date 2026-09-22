from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    department: str = Field(min_length=1)
    primary_skill: str = Field(min_length=1)
    location: str = Field(min_length=1)
    work_mode: Literal["WFH", "WFO"]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "chandu",
                "email": "chandu@gmail.com",
                "department": "Development",
                "primary_skill": "Python",
                "location": "Mandya",
                "work_mode": "WFO"
            }
        }
    )


class EmployeeUpdate(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    department: str = Field(min_length=1)
    primary_skill: str = Field(min_length=1)
    location: str = Field(min_length=1)
    work_mode: Literal["WFH", "WFO"]

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Chandu Updated",
                "email": "chandu@gmail.com",
                "department": "Development",
                "primary_skill": "Python",
                "location": "Mandya",
                "work_mode": "WFO"
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
    work_mode: Literal["WFH", "WFO"]
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)