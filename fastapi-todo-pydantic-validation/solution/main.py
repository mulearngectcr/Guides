from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI()

todos = []
id_counter = 1


class Todo(BaseModel):
    title: str = Field(min_length=1)
    checked: bool = False
    priority: Literal["low", "medium", "high"] = "medium"


@app.get("/todos")
def get_todos():
    return todos


@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    global id_counter

    new_todo = todo.dict()
    new_todo["id"] = id_counter

    todos.append(new_todo)

    id_counter += 1

    return {
        "message": "Todo added successfully"
    }


@app.get("/todos/{id}")
def get_todo(id: int):
    for todo in todos:
        if todo["id"] == id:
            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


@app.put("/todos/{id}")
def update_todo(id: int, updated_todo: Todo):
    for todo in todos:
        if todo["id"] == id:
            todo["title"] = updated_todo.title
            todo["checked"] = updated_todo.checked
            todo["priority"] = updated_todo.priority

            return {
                "message": "Todo updated successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


@app.delete("/todos/{id}")
def delete_todo(id: int):
    for todo in todos:
        if todo["id"] == id:
            todos.remove(todo)

            return {
                "message": "Todo deleted successfully"
            }

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )
