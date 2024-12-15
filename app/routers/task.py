from fastapi import APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import insert, select, update, delete
from app.backend.db_depends import get_db
from app.models import *
from app.schemas import CreateTask, UpdateTask
from slugify import slugify

router = APIRouter(prefix="/task", tags=["task"])

@router.get("/all_tasks")
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks

@router.get("/task_id")
async def task_by_id(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(Task.id == task_id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    else:
        return task

@router.post("/create")
async def create_task(db: Annotated[Session, Depends(get_db)],create_task: CreateTask, user_id: int ):
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User was not found")
    db.execute(insert(Task).values(priority=create_task.priority,
                                   user_id=user_id,
                                   content=create_task.content,
                                   title=create_task.title,
                                   slug=slugify(create_task.title)
                                   ))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
            }

@router.put("/update")
async def update_task(db: Annotated[Session, Depends(get_db)], task_id: int, update_task: UpdateTask):
    task = db.scalar(select(Task).where(task_id == Task.id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )

    db.execute(update(Task).where(task_id == Task.id).values(
        title=update_task.title,
        content=update_task.content,
        priority=update_task.priority
    ))

    db.commit()
    return  {'status_code': status.HTTP_200_OK,
             'transaction': 'Task update is successful!'}

@router.delete("/delete")
async def delete_task(db: Annotated[Session, Depends(get_db)], task_id: int):
    task = db.scalar(select(Task).where(task_id == Task.id))
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task was not found"
        )
    db.execute(delete(Task).where(task_id == Task.id))

    db.commit()
    return {'status_code': status.HTTP_200_OK,
            'transaction': 'Task delete is successful!'}