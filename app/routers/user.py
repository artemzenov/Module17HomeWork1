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
from app.schemas import CreateUser
from app.schemas import UpdateUser


router = APIRouter(prefix='/user', tags=['user'])


@router.get('/')
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalars(select(User)).all()
    return users


@router.get('/user_id')
async def user_by_id(db: Annotated[Session, Depends(get_db)],
                     user_id: int):
    if db.scalar(select(User).where(User.id == user_id)):
        return db.scalar(select(User).where(User.id == user_id))
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User in not found'
            )


@router.post('/create')
async def create_user(db: Annotated[Session, Depends(get_db)],
                      create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slugify(create_user.username)))
    db.commit()
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'Successful'
        }


@router.put('/update')
async def update_user(db: Annotated[Session, Depends(get_db)],
                      update_user: UpdateUser,
                      user_id: int):
    if db.scalar(select(User).where(User.id == user_id)):
        db.execute(update(User).where(User.id == user_id).values(
            firstname=update_user.firstname,
            lastname=update_user.lastname,
            age=update_user.age
            ))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User update is successfull!'
            }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )


@router.delete('/delete')
async def delete_user(db: Annotated[Session, Depends(get_db)],
                      user_id: int):
    if db.scalar(select(User).where(User.id == user_id)):
        db.execute(delete(User).where(User.id == user_id))
        db.commit()
        return {
            'status_code': status.HTTP_200_OK,
            'transaction': 'User delete is successfull!'
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User was not found'
        )
