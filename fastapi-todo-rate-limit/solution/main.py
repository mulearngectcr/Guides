"""
Rate limiting is added using slowapi.
A global limit of 10 requests per minute applies to all endpoints.
POST /todos has a stricter limit of 3 requests per minute since it is a write operation.
"""
from fastapi import FastAPI, HTTPException, Security, Depends, Request
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from typing import Literal
from dotenv import load_dotenv
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")
api_key_scheme = APIKeyHeader(name="X-API-Key")

limiter = Limiter(key_func=get_remote_address, default_limits=["10/minute"])

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

todos = []
id_counter = 1


class Todo(BaseModel):
    title: str = Field(min_length=1)
    checked: bool = False
    priority: Literal["low", "medium", "high"] = "medium"


def authenticate(api_key: str = Security(api_key_scheme)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid API Key"
        )


@app.get("/todos", dependencies=[Depends(authenticate)])
def get_todos():
    return todos


@app.post("/todos", status_code=201, dependencies=[Depends(authenticate)])
@limiter.limit("3/minute")
async def create_todo(request: Request, todo: Todo):
    global id_counter
    new_todo = todo.model_dump()
    new_todo["id"] = id_counter
    todos.append(new_todo)
    id_counter += 1
    return {
        "message": "Todo added successfully"
    }


@app.get("/todos/{id}", dependencies=[Depends(authenticate)])
def get_todo(id: int):
    for todo in todos:
        if todo["id"] == id:
            return todo
    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )


@app.put("/todos/{id}", dependencies=[Depends(authenticate)])
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


@app.delete("/todos/{id}", dependencies=[Depends(authenticate)])
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
