import uuid
from typing import Any
from datetime import date, datetime

from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, UserUpdate, Department, Employee, TimeSheet, LeaveRequest, UserRole, LeaveStatus


def create_user(*, session: Session, user_create: UserCreate) -> User:
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def update_user(*, session: Session, db_user: User, user_in: UserUpdate) -> Any:
    user_data = user_in.model_dump(exclude_unset=True)
    extra_data = {}
    if "password" in user_data:
        password = user_data["password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate(*, session: Session, email: str, password: str) -> User | None:
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


# Department CRUD

def create_department(session: Session, name: str, description: str | None = None, 
                      manager_id: uuid.UUID | None = None) -> Department:
    department = Department(name=name, description=description, manager_id=manager_id)
    session.add(department)
    session.commit()
    session.refresh(department)
    return department

def get_departments(session: Session) -> list[Department]:
    return session.exec(select(Department)).all()

def get_department(session: Session, department_id: uuid.UUID) -> Department | None:
    return session.get(Department, department_id)

def update_department(session: Session, department_id: uuid.UUID, 
                      name: str | None = None, description: str | None = None, 
                      manager_id: uuid.UUID | None = None) -> Department | None:
    department = session.get(Department, department_id)
    if not department:
        return None
    if name:
        department.name = name
    if description:
        department.description = description
    if manager_id:
        department.manager_id = manager_id
    session.add(department)
    session.commit()
    session.refresh(department)
    return department

def delete_department(session: Session, department_id: uuid.UUID) -> bool:
    department = session.get(Department, department_id)
    if not department:
        return False
    employees = session.exec(select(Employee).where(Employee.department_id == department_id)).all()
    if employees:
        raise Exception("Нельзя удалить отдел с сотрудниками. Сначала удалите или переведите сотрудников.")
    session.delete(department)
    session.commit()
    return True

# Employee CRUD

def create_employee(session: Session, user_id: uuid.UUID, 
                    department_id: uuid.UUID, position: str, hire_date: date, 
                    phone: str | None = None, salary: float | None = None) -> Employee:
    employee = Employee(user_id=user_id, department_id=department_id, 
                        position=position, hire_date=hire_date, 
                        phone=phone, salary=salary)
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

def get_employees(session: Session, department_id: uuid.UUID | None = None, 
                  position: str | None = None) -> list[Employee]:
    statement = select(Employee)
    if department_id:
        statement = statement.where(Employee.department_id == department_id)
    if position:
        statement = statement.where(Employee.position == position)
    return session.exec(statement).all()

def get_employee(session: Session, employee_id: uuid.UUID) -> Employee | None:
    return session.get(Employee, employee_id)

def update_employee(session: Session, employee_id: uuid.UUID, **kwargs) -> Employee | None:
    employee = session.get(Employee, employee_id)
    if not employee:
        return None
    for key, value in kwargs.items():
        if hasattr(employee, key):
            setattr(employee, key, value)
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

def delete_employee(session: Session, employee_id: uuid.UUID) -> bool:
    employee = session.get(Employee, employee_id)
    if not employee:
        return False
    session.delete(employee)
    session.commit()
    return True

def deactivate_employee(session: Session, employee_id: uuid.UUID) -> Employee | None:
    employee = session.get(Employee, employee_id)
    if not employee:
        return None
    employee.is_active = False
    session.add(employee)
    session.commit()
    session.refresh(employee)
    return employee

# TimeSheet CRUD

def create_timesheet(session: Session, employee_id: uuid.UUID, date: date, check_in: datetime | None = None, check_out: datetime | None = None) -> TimeSheet:
    timesheet = TimeSheet(employee_id=employee_id, date=date, check_in=check_in, check_out=check_out)
    session.add(timesheet)
    session.commit()
    session.refresh(timesheet)
    return timesheet

def get_timesheets(session: Session, employee_id: uuid.UUID, start_date: date, end_date: date) -> list[TimeSheet]:
    statement = select(TimeSheet).where(TimeSheet.employee_id == employee_id, TimeSheet.date >= start_date, TimeSheet.date <= end_date)
    return session.exec(statement).all()

# LeaveRequest CRUD

def get_leave_request(session: Session, request_id: uuid.UUID) -> LeaveRequest | None:
    return session.get(LeaveRequest, request_id)

def create_leave_request(session: Session, employee_id: uuid.UUID, 
                         leave_type: str, start_date: date, end_date: date, 
                         approved_by_manager_id: uuid.UUID | None = None) -> LeaveRequest:
    leave_request = LeaveRequest(employee_id=employee_id, leave_type=leave_type, 
                                 start_date=start_date, end_date=end_date)
    if approved_by_manager_id:
        leave_request.status = LeaveStatus.APPROVED
        leave_request.approved_by_manager_id = approved_by_manager_id
    session.add(leave_request)
    session.commit()
    session.refresh(leave_request)
    return leave_request

def update_leave_request_status(session: Session, request_id: uuid.UUID, 
                                status: LeaveStatus, approved_by_manager_id: 
                                uuid.UUID | None = None) -> LeaveRequest | None:
    leave_request = session.get(LeaveRequest, request_id)
    if not leave_request:
        return None
    leave_request.status = status
    if approved_by_manager_id:
        leave_request.approved_by_manager_id = approved_by_manager_id
    session.add(leave_request)
    session.commit()
    session.refresh(leave_request)
    return leave_request

def get_leave_requests(session: Session, status: LeaveStatus | None = None) -> list[LeaveRequest]:
    statement = select(LeaveRequest)
    if status:
        statement = statement.where(LeaveRequest.status == status)
    return session.exec(statement).all()
