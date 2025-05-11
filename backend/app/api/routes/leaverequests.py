from fastapi import APIRouter, Depends, HTTPException, status, Body
from sqlmodel import Session
from typing import List
from datetime import date
from app import crud
from app.models import LeaveRequest, LeaveStatus, LeaveType, User, UserRole, Employee
from app.api.deps import get_current_active_user, get_session

router = APIRouter()

# Подача заявки на отпуск/больничный (только сотрудник)
@router.post("/leaverequests", response_model=LeaveRequest, tags=["leaverequests"])
def create_leave_request(
    leave_type: LeaveType = Body(...),
    start_date: date = Body(...),
    end_date: date = Body(...),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    if current_user.role != UserRole.EMPLOYEE:
        raise HTTPException(status_code=403, detail="Только для сотрудников")
    employee = session.exec(crud.get_employees(session, None, None))
    employee_obj = None
    for e in employee:
        if e.user_id == current_user.id:
            employee_obj = e
            break
    if not employee_obj:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return crud.create_leave_request(session, employee_obj.id, leave_type, start_date, end_date)

# Просмотр заявок (админ и менеджер — все, сотрудник — только свои)
@router.get("/leaverequests", response_model=List[LeaveRequest], tags=["leaverequests"])
def get_leave_requests(
    status: LeaveStatus = None,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    if current_user.role in [UserRole.ADMIN, UserRole.MANAGER]:
        return crud.get_leave_requests(session, status)
    elif current_user.role == UserRole.EMPLOYEE:
        # Только свои заявки
        employee = session.exec(crud.get_employees(session, None, None))
        employee_obj = None
        for e in employee:
            if e.user_id == current_user.id:
                employee_obj = e
                break
        if not employee_obj:
            return []
        return [req for req in crud.get_leave_requests(session, status) if req.employee_id == employee_obj.id]
    else:
        raise HTTPException(status_code=403, detail="Недостаточно прав")

# Подтверждение/отклонение заявки (только менеджер отдела сотрудника)
@router.patch("/leaverequests/{request_id}", response_model=LeaveRequest, tags=["leaverequests"])
def update_leave_request_status(
    request_id: str,
    status: LeaveStatus,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    leave_request = crud.get_leave_request(session, request_id)
    if not leave_request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    employee = crud.get_employee(session, leave_request.employee_id)
    department = crud.get_department(session, employee.department_id)
    if current_user.role == UserRole.MANAGER:
        if department.manager_id != current_user.id:
            raise HTTPException(status_code=403, detail="Менеджер может согласовывать только заявки своих сотрудников")
    else:
        raise HTTPException(status_code=403, detail="Только менеджер отдела может согласовывать заявки")
    return crud.update_leave_request_status(session, request_id, status, approved_by_manager_id=current_user.id)

# Назначить отпуск сотруднику (только менеджер отдела)
@router.post("/leaverequests/assign", response_model=LeaveRequest, tags=["leaverequests"])
def assign_leave_to_employee(
    employee_id: str = Body(...),
    leave_type: LeaveType = Body(...),
    start_date: date = Body(...),
    end_date: date = Body(...),
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    employee = crud.get_employee(session, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    department = crud.get_department(session, employee.department_id)
    if current_user.role == UserRole.MANAGER:
        if department.manager_id != current_user.id:
            raise HTTPException(status_code=403, detail="Менеджер может назначать отпуск только своим сотрудникам")
    elif current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Только менеджер отдела или админ может назначать отпуск")
    return crud.create_leave_request(session, employee.id, leave_type, start_date, end_date, approved_by_manager_id=current_user.id)

# Удаление отпуска (только для админа и менеджера)
@router.delete("/leaverequests/{request_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["leaverequests"])
def delete_leave_request(
    request_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    leave_request = crud.get_leave_request(session, request_id)
    if not leave_request:
        raise HTTPException(status_code=404, detail="Заявка не найдена")
    # Только админ или менеджер отдела сотрудника
    employee = crud.get_employee(session, leave_request.employee_id)
    department = crud.get_department(session, employee.department_id)
    if current_user.role == UserRole.ADMIN or (current_user.role == UserRole.MANAGER and department.manager_id == current_user.id):
        session.delete(leave_request)
        session.commit()
        return
    raise HTTPException(status_code=403, detail="Нет прав на удаление заявки")
