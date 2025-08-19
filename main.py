from fastapi import FastAPI

api = FastAPI()


# first versy simple api to print out"hello world" in page
@api.get('/')
def index():
    return {'message': 'hello world'}



# sample project of a todo list to learn fastapi
# in this project instead of connecting to a dib , for simplicity we use a list as storage of our data
all_todos = [
    {"todo_id": 1, "todo_name": "Buy groceries", "todo_description": "Milk, eggs, and bread"},
    {"todo_id": 2, "todo_name": "Read book", "todo_description": "Finish chapter 5 of Python book"},
    {"todo_id": 3, "todo_name": "Workout", "todo_description": "30 minutes of cardio"},
    {"todo_id": 4, "todo_name": "Email client", "todo_description": "Send project update email"},
    {"todo_id": 5, "todo_name": "Clean desk", "todo_description": "Organize papers and supplies"}
]


@api.get('/todos/{todo_id}') # todo_id is a path parameter which is define iside {}
def todo(todo_id: int):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            return todo
        
    return {'result':f"not found {todo_id} - > {todo['todo_id']} > todo:{todo}"}
        

@api.get('/todos') # first_n is query parameter which not appears in url > urs will be like : localhost:port/todos?firstn=3
def todos(first_n: int = None): # default value is None
    if first_n:
        return all_todos[:first_n]
    else:
        return all_todos


#-------- without pydantic -->> !!!!! an inefficient way !!!!!!! -------------
# normally we do not use this method 
# apost method:
@api.post('/todos')
def create_todo(todo: dict):
    new_todo_id= max(todo['todo_id'] for todo in all_todos)+1

    new_todo = {
        'todo_id': new_todo_id,
        'todo_name': todo['todo_name'],
        'todo_description': todo['todo_description'],
    }
    
    all_todos.append(new_todo)
    return new_todo 


@api.put('/todos/{todo_id}')
def update_todo(todo_id: int, updated_todo: dict):
    for todo in all_todos:
        if todo['todo_id'] == todo_id:
            todo['todo_name'] = updated_todo['todo_name']
            todo['todo_description'] = updated_todo['todo_description']
            return todo
    return 'Error not found'


@api.delete('/todos/{todo_id}')
def delete_todo(todo_id: int):
    for index , todo in enumerate(all_todos):
        if todo['todo_id'] == todo_id:
            deleted_todos = all_todos.pop(index)
            return deleted_todos
    return 'Error not found'


        