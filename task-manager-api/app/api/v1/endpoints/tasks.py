from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_active_user, get_db
from app.models.task import TaskStatus, TaskPriority
from app.models.user import User
from app.schemas.task import TaskCreate, TaskOut, TaskUpdate
from app.services import task_service

router = APIRouter()


@router.get("/", response_model=List[TaskOut])
async def read_tasks(
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    priority_filter: Optional[TaskPriority] = Query(None, alias="priority"),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    tasks = await task_service.get_user_tasks(
        db, owner_id=current_user.id, status=status_filter, priority=priority_filter, skip=skip, limit=limit
    )
    return tasks


@router.post("/", response_model=TaskOut, status_code=status.HTTP_201_CREATED)
async def create_new_task(
    task_in: TaskCreate,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = await task_service.create_task(db, task_in=task_in, owner_id=current_user.id)
    return task


@router.get("/{task_id}", response_model=TaskOut)
async def read_task_by_id(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = await task_service.get_task_by_id(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    return task


@router.put("/{task_id}", response_model=TaskOut)
async def update_existing_task(
    task_id: int,
    task_in: TaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = await task_service.get_task_by_id(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    task = await task_service.update_task(db, task=task, task_in=task_in)
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_existing_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    task = await task_service.get_task_by_id(db, task_id=task_id, owner_id=current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Tâche introuvable")
    await task_service.delete_task(db, task=task)
    return None
