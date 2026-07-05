"""
This authentication implementation is intentionally kept simple to help you understand the basic concepts.

In real-world applications, developers typically use more robust authentication methods such as JWT tokens,
database-stored API keys, OAuth2, or session-based authentication systems.
"""


from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

API_KEY = os.getenv("API_KEY")

todos = []
id_counter = 1


class Todo(BaseModel):
    title: str = Field(min_length=1)
    checked: bool = False
    priority: Literal["low", "medium", "high"] = "medium"


def authenticate(x_api_key: str = Header()):

    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )


@app.get("/todos")
def get_todos(x_api_key: str = Header()):

    authenticate(x_api_key)

    return todos


@app.post("/todos", status_code=201)
def create_todo(todo: Todo, x_api_key: str = Header()):

    authenticate(x_api_key)

    global id_counter

    new_todo = todo.model_dump()
    new_todo["id"] = id_counter

    todos.append(new_todo)

    id_counter += 1

    return {
        "message": "Todo added successfully"
    }


@app.get("/todos/{id}")
def get_todo(id: int, x_api_key: str = Header()):

    authenticate(x_api_key)

    for todo in todos:
        if todo["id"] == id:
            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


@app.put("/todos/{id}")
def update_todo(id: int, updated_todo: Todo, x_api_key: str = Header()):

    authenticate(x_api_key)

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
def delete_todo(id: int, x_api_key: str = Header()):

    authenticate(x_api_key)

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