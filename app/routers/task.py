from fastapi import APIRouter
from fastapi import Depends
from fastapi import status
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy import delete
from typing import Annotated
from slugify import slugify
from app.backend.db_depends import get_db
from app.models import User
from app.models import Task
from app.schemas import CreateUser
from app.schemas import UpdateUser
from app.schemas import CreateTask
from app.schemas import UpdateTask


router = APIRouter(prefix='/task', tags=['task'])


@router.get('/')
async def all_tasks(db: Annotated[Session, Depends(get_db)]):
    tasks = db.scalars(select(Task)).all()
    return tasks


@router.get('/task_id')
async def task_by_id(db: Annotated[Session, Depends(get_db)],
                     task_id: int):
    if db.scalar(select(Task).where(Task.id == task_id)):
        return db.scalar(select(Task).where(Task.id == task_id))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task is not found'
            )


@router.post('/create')
async def create_task(db: Annotated[Session, Depends(get_db)],
                      create_task: CreateTask,
                      user_id: int):
    if db.scalar(select(User).where(User.id == user_id)):
        db.execute(insert(Task).values(title=create_task.title,
                                       content=create_task.content,
                                       priority=create_task.priority,
                                       user_id=user_id,
                                       slug=slugify(create_task.title)))
        db.commit()
        return {
            'status_code': status.HTTP_201_CREATED,
            'transaction': 'Successful'
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
            )


@router.put('/update')
async def update_task(db: Annotated[Session, Depends(get_db)],
                      update_task: UpdateTask,
                      task_id: int):
    if db.scalar(select(Task).where(Task.id == task_id)):
        db.execute(update(Task).where(Task.id == task_id).values(title=update_task.title,
                                                                 content=update_task.content,
                                                                 priority=update_task.priority))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task update is successful'
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task is not found'
            )


@router.delete('/delete')
async def delete_task(db: Annotated[Session, Depends(get_db)],
                      task_id: int):
    if db.scalar(select(Task).where(Task.id == task_id)):
        db.execute(delete(Task).where(Task.id == task_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'Task delete is successful'
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Task is not found'
            )
