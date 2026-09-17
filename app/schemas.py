from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from enum import Enum


class WorkMode(str, Enum):
    WFH = "WFH"
    WFO = "WFO"


class EmployeeCreate(BaseModel):
    name: str
    email: EmailStr
    department: str
    primary_skill: str
    location: str
    work_mode: WorkMode
    is_active: bool = True


class EmployeeResponse(EmployeeCreate):
    id: int
    created_at: datetime


class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    department: Optional[str] = None
    primary_skill: Optional[str] = None
    location: Optional[str] = None
    work_mode: Optional[WorkMode] = None
    is_active: Optional[bool] = None
