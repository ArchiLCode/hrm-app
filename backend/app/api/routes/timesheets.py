from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from datetime import date, datetime
from app import crud
from app.models import TimeSheet, User, UserRole, Employee
from app.api.deps import get_current_active_user, get_session

router = APIRouter()

# Фиксация времени прихода/ухода (только сотрудник)
@router.post("/timesheets/check", response_model=TimeSheet)
def check_in_out(
    check_in: bool,  # True - приход, False - уход
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    if current_user.role != UserRole.EMPLOYEE:
        raise HTTPException(status_code=403, detail="Только для сотрудников")
    # Получить сотрудника по user_id
    employee = session.exec(
        crud.get_employees(session, None, None)
    )
    employee_obj = None
    for e in employee:
        if e.user_id == current_user.id:
            employee_obj = e
            break
    if not employee_obj:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    today = date.today()
    # Найти или создать табель на сегодня
    timesheets = crud.get_timesheets(session, employee_obj.id, today, today)
    if timesheets:
        timesheet = timesheets[0]
    else:
        timesheet = crud.create_timesheet(session, employee_obj.id, today)
    now = datetime.now()
    if check_in:
        timesheet.check_in = now
    else:
        timesheet.check_out = now
    session.add(timesheet)
    session.commit()
    session.refresh(timesheet)
    return timesheet

# Просмотр табеля за период (менеджер/админ)
@router.get("/timesheets/{employee_id}", response_model=List[TimeSheet])
def get_timesheet_for_employee(
    employee_id: str,
    start_date: date,
    end_date: date,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return crud.get_timesheets(session, employee_id, start_date, end_date)
