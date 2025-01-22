from pydantic import BaseModel
from pydantic import Field


class UpdateUser(BaseModel):
    firstname:str = Field(default='Ivan')
    lastname: str = Field(default='Ivanov')
    age: int = Field(default=25)


class CreateUser(UpdateUser):
    username: str = Field(default='ivan')


class CreateTask(BaseModel):
    title: str = Field(default='Homework')
    content: str = Field(default='Task 1: Math')
    priority: str = Field(default='Monday 18:00')


class UpdateTask(CreateTask):
    pass
