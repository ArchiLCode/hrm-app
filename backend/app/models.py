import uuid
from datetime import date, datetime
from enum import Enum

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class UserRole(str, Enum):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"


class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    role: UserRole = Field(default=UserRole.EMPLOYEE, index=True)
    employee: "Employee" = Relationship(back_populates="user")


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)
    role: UserRole = Field(default=UserRole.EMPLOYEE)
    department_id: uuid.UUID | None = None  # Необязательное поле для поддержки менеджеров


class UserRegister(SQLModel):
    email: EmailStr = Field(max_length=255)
    password: str = Field(min_length=8, max_length=40)
    full_name: str | None = Field(default=None, max_length=255)


# Properties to receive via API on update, all are optional
class UserUpdate(UserBase):
    email: EmailStr | None = Field(default=None, max_length=255)  # type: ignore
    password: str | None = Field(default=None, min_length=8, max_length=40)


class UserUpdateMe(SQLModel):
    full_name: str | None = Field(default=None, max_length=255)
    email: EmailStr | None = Field(default=None, max_length=255)


class UpdatePassword(SQLModel):
    current_password: str = Field(min_length=8, max_length=40)
    new_password: str = Field(min_length=8, max_length=40)


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID
    role: UserRole


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str = Field(min_length=8, max_length=40)


# Модель отдела
class Department(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=100, unique=True, index=True)
    description: str | None = Field(default=None, max_length=255)
    manager_id: uuid.UUID = Field(foreign_key="user.id")  # Менеджер-владелец отдела
    employees: list["Employee"] = Relationship(back_populates="department")


# Модель сотрудника
class Employee(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", unique=True)
    department_id: uuid.UUID = Field(foreign_key="department.id")
    position: str = Field(max_length=100)
    hire_date: date
    phone: str | None = Field(default=None, max_length=20)
    salary: float | None = None
    is_active: bool = True
    user: User = Relationship(back_populates="employee")
    department: Department = Relationship(back_populates="employees")
    timesheets: list["TimeSheet"] = Relationship(back_populates="employee")
    leave_requests: list["LeaveRequest"] = Relationship(back_populates="employee")


# Табель рабочего времени
class TimeSheet(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    employee_id: uuid.UUID = Field(foreign_key="employee.id")
    date: date
    check_in: datetime | None = None
    check_out: datetime | None = None
    employee: Employee = Relationship(back_populates="timesheets")


# Заявка на отпуск/больничный
class LeaveType(str, Enum):
    VACATION = "vacation"
    SICK_LEAVE = "sick_leave"


class LeaveStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"


class LeaveRequest(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    employee_id: uuid.UUID = Field(foreign_key="employee.id")
    leave_type: LeaveType
    start_date: date
    end_date: date
    status: LeaveStatus = Field(default=LeaveStatus.PENDING)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    approved_by_manager_id: uuid.UUID | None = Field(default=None, foreign_key="user.id")  # Кто согласовал (менеджер)
    employee: Employee = Relationship(back_populates="leave_requests")


# Pydantic-схема для создания отдела
class DepartmentCreate(SQLModel):
    name: str
    description: str | None = None
    manager_id: uuid.UUID | None = None
