from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import List
from app import crud
from app.models import Department, User, UserRole, DepartmentCreate
from app.api.deps import get_current_active_user, get_session

router = APIRouter()

# Получить список отделов
@router.get("/departments", response_model=List[Department], tags=["departments"])
def read_departments(
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    return crud.get_departments(session)

# Получить отдел по id
@router.get("/departments/{department_id}", response_model=Department, tags=["departments"])
def read_department(
    department_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    department = crud.get_department(session, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Отдел не найден")
    return department

# Создать отдел
@router.post("/departments", response_model=Department, tags=["departments"])
def create_department(
    department: DepartmentCreate,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    if current_user.role not in [UserRole.ADMIN, UserRole.MANAGER]:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    manager_id = department.manager_id or current_user.id
    if current_user.role == UserRole.MANAGER and manager_id != current_user.id:
        raise HTTPException(status_code=403, detail="Менеджер может создавать отдел только для себя")
    return crud.create_department(session, name=department.name, description=department.description, manager_id=manager_id)

# Обновить отдел (админ или менеджер только свой)
@router.patch("/departments/{department_id}", response_model=Department, tags=["departments"])
def update_department(
    department_id: str,
    department_update: dict,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    department = crud.get_department(session, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Отдел не найден")
    if current_user.role == UserRole.ADMIN:
        pass
    elif current_user.role == UserRole.MANAGER:
        if department.manager_id != current_user.id:
            raise HTTPException(status_code=403, detail="Менеджер может редактировать только свои отделы")
    else:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    return crud.update_department(session, department_id, **department_update)

# Удалить отдел (админ или менеджер только свой)
@router.delete("/departments/{department_id}", tags=["departments"])
def delete_department(
    department_id: str,
    current_user: User = Depends(get_current_active_user),
    session: Session = Depends(get_session),
):
    department = crud.get_department(session, department_id)
    if not department:
        raise HTTPException(status_code=404, detail="Отдел не найден")
    if current_user.role == UserRole.ADMIN:
        pass
    elif current_user.role == UserRole.MANAGER:
        if department.manager_id != current_user.id:
            raise HTTPException(status_code=403, detail="Менеджер может удалять только свои отделы")
    else:
        raise HTTPException(status_code=403, detail="Недостаточно прав")
    try:
        if not crud.delete_department(session, department_id):
            raise HTTPException(status_code=404, detail="Отдел не найден")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"ok": True}
