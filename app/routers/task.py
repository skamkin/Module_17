from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing import Annotated
from app.models import *
from app.schemas import CreateTask, UpdateTask
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_task(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)],
                     task_id: int):
    tasks = db.scalars(select(Task).where(Task.id == task_id))
    for task in tasks:
        if task is not None:
            return task

    raise HTTPException(status_code=404, detail="User was not found")




@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)], create_task: CreateTask, user_id: int):
    users = db.scalars(select(User).where(User.id == user_id))
    if users is None:
        raise HTTPException(status_code=404, detail="User was not found")
    db.execute(insert(Task).values(title=create_task.title,
                                   content=create_task.content,
                                   priority=create_task.priority,
                                   user_id=user_id,
                                   slug=slugify(create_task.title)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED, 'transaction': 'Successful'}


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int,
                      update_task: UpdateTask):
    for task in tasks:
        if task is None:
            db.execute(update(Task).where(Task.id==task_id).values(
                title=update_task.title,
                content=update_task.content,
                priority=update_task.priority
            ))
            db.commit()
            return {
                'status_code': status.HTTP_200_OK,
                'transaction': 'User update is successful!'
            }

    raise HTTPException(status_code=404, detail="User was not found")



@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int):
    task = db.get(Task, task_id)
    if task is not None:
        db.delete(task)
        db.commit()

    return {'status_code': status.HTTP_200_OK, 'transaction': 'Task delete is successful!'}
    raise HTTPException(status_code=404, detail="Task was not found")
