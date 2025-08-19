from typing import List, Optional
from enum import IntEnum

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field 

api = FastAPI()

class Priority(IntEnum): ## a new type of data is created which could have just 3 values : 1,2,3
    LOW=3
    MEDIUM=2
    HIGH=1

class TodoBase(BaseModel): # other models will inherit from this base class which has common fields
    todo_name: str = Field(..., min_length=3, max_laength=512, description='Name of the Todo')
    todo_description: str = Field(..., description='Desciption of todos')
    priority: Priority = Field(default=Priority.LOW, description='the priority of todo')


class Todo(TodoBase): #will be uset for get method
    todo_id: int = Field(..., description='the unique id of todo')


class TodoCreate(TodoBase): # will be used for post method
    pass

class TodoUpdate(BaseModel): # not inherited from TodoBase since data types is optional and user will not forced to insert all feields if he wants to update just a few of fields
    todo_name: Optional[str] = Field(None, min_length=3, max_length=512, description='Name of the Todo')
    todo_description: Optional[str] = Field(None, description='Desciption of todos')
    priority: Optional[Priority] = Field(None, description='the priority of todo')



@api.get('/')
def home():
    return {'msg': 'welcome home'}


# for this learning project we use a list of data nstead of DB
all_todos = [
    Todo(todo_id=1, todo_name='sport', todo_description='sport description',),
    Todo(todo_id=2, todo_name='study', todo_description='std description',),
    Todo(todo_id=3, todo_name='programming', todo_description='prg description',),
    Todo(todo_id=4, todo_name='movie', todo_description='mv description',),
    Todo(todo_id=5, todo_name='emails', todo_description='em description',),
]

@api.get('/todos/{todo_id}', response_model=Todo)
def get_todo(todo_id: int,):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            return todo
        
    raise HTTPException(status_code=404, detail='todo not found')


@api.get('/todos', response_model=List[Todo])
def get_todos(first_n: int = None):
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos
    

@api.post('/todos', response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo_id = max(todo.todo_id for todo in all_todos) + 1

    new_todo = Todo(todo_id=new_todo_id, todo_name=todo.todo_name, todo_description=todo.todo_description, priority=todo.priority)

    all_todos.append(new_todo)
    return new_todo 


@api.put('/todos/{todo_id}', response_model=Todo)
def update_todo(todo_id: int, updated_todo: TodoUpdate):
    for todo in all_todos:
        if todo.todo_id == todo_id:
            if updated_todo.todo_name is not None:
                todo.todo_name = updated_todo.todo_name
            if updated_todo.todo_description is not None:
                todo.todo_description = updated_todo.todo_description
            if updated_todo.priority is not None:
                todo.priority = updated_todo.priority
            return todo
    raise HTTPException (status_code=404, detail='todo not found')


@api.delete('/todos/{todo_id}', response_model=Todo)
def delete_todo(todo_id: int):
    for index , todo in enumerate(all_todos):
        if todo.todo_id == todo_id:
            deleted_todo=all_todos.pop(index)
            return deleted_todo
        
    raise HTTPException (status_code=404, detail='todo not found')

