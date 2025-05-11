from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
from app import crud
from app.models import Employee, User, UserRole
from app.api.deps import get_current_active_user, get_session

router = APIRouter()

# Получить список сотрудников (видят все авторизованные, фильтрация по отделу/должности)
@router.get("/employees", response_model=List[dict], tags=["employees"])
def read_employees(
    department_id: str = None,
    position: str = None,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    employees = crud.get_employees(session, department_id, position)
    # Получаем user_id всех сотрудников
    user_ids = [e.user_id for e in employees]
    users = session.exec(select(User).where(User.id.in_(user_ids))).all()
    user_map = {str(u.id): u.full_name or u.email for u in users}
    # Добавляем user_name в ответ
    result = []
    for e in employees:
        emp_dict = e.dict()
        emp_dict["user_name"] = user_map.get(str(e.user_id), str(e.user_id))
        result.append(emp_dict)
    return result

# Получить данные о себе (сотрудник)
@router.get("/employees/me", response_model=Employee, tags=["employees"])
def read_my_employee(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    employees = crud.get_employees(session, None, None)
    for e in employees:
        if e.user_id == current_user.id:
            return e
    raise HTTPException(status_code=404, detail="Сотрудник не найден")

# Добавить сотрудника (админ — в любой отдел, менеджер — только в свой)
@router.post("/employees", response_model=Employee, tags=["employees"])
def create_employee(
    employee: Employee,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    department = crud.get_department(session, employee.department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Отдел не найден")
    if current_user.role == UserRole.ADMIN:
        pass
    elif current_user.role == UserRole.MANAGER:
        if department.manager_id != current_user.id:
            raise HTTPException(status_code=403, detail="Менеджер может добавлять сотрудников только в свои отделы")
    else:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    # Проверка: сотрудник может быть только в одном отделе
    existing = crud.get_employees(session, None, None)
    for e in existing:
        if e.user_id == employee.user_id:
            raise HTTPException(status_code=400, detail="Сотрудник уже состоит в отделе")
    return crud.create_employee(
        session,
        user_id=employee.user_id,
        department_id=employee.department_id,
        position=employee.position,
        hire_date=employee.hire_date,
        phone=employee.phone,
        salary=employee.salary,
    )

# Редактировать сотрудника (админ — любого, менеджер — только своих и только между своими отделами)
@router.patch("/employees/{employee_id}", response_model=Employee, tags=["employees"])
def update_employee(
    employee_id: str,
    employee_update: dict,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    employee = crud.get_employee(session, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    if current_user.role == UserRole.ADMIN:
        pass
    elif current_user.role == UserRole.MANAGER:
        # Менеджер может редактировать только своих сотрудников и переводить только между своими отделами
        dept_from = crud.get_department(session, employee.department_id)
        dept_to = None
        if "department_id" in employee_update:
            dept_to = crud.get_department(session, employee_update["department_id"])
        if dept_from.manager_id != current_user.id or (dept_to and dept_to.manager_id != current_user.id):
            raise HTTPException(status_code=403, detail="Менеджер может переводить только между своими отделами")
    else:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    # Проверка: сотрудник может быть только в одном отделе
    if "department_id" in employee_update:
        existing = crud.get_employees(session, None, None)
        for e in existing:
            if e.user_id == employee.user_id and str(e.id) != employee_id:
                raise HTTPException(status_code=400, detail="Сотрудник уже состоит в отделе")
    return crud.update_employee(session, employee_id, **employee_update)

# Деактивировать сотрудника (уволить, админ — любого, менеджер — только своих)
@router.delete("/employees/{employee_id}", tags=["employees"])
def delete_employee(
    employee_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    employee = crud.get_employee(session, employee_id)
    if not employee:
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    if current_user.role == UserRole.ADMIN:
        pass
    elif current_user.role == UserRole.MANAGER:
        dept = crud.get_department(session, employee.department_id)
        if dept.manager_id != current_user.id:
            raise HTTPException(status_code=403, detail="Менеджер может увольнять только своих сотрудников")
    else:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    if not crud.delete_employee(session, employee.id):
        raise HTTPException(status_code=404, detail="Сотрудник не найден")
    return {"ok": True}
