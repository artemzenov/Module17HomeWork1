from fastapi import FastAPI
from app.routers import task
from app.routers import user


app = FastAPI()

app.include_router(task.router)
app.include_router(user.router)


@app.get('/')
async def welcome() -> dict:
    return {'message': 'Welcome to Taskmanager'}

#Для тестирования - Распечатываем SQL запрос
from sqlalchemy.schema import CreateTable
from app.models import *

print(CreateTable(User.__table__))
print(CreateTable(Task.__table__))