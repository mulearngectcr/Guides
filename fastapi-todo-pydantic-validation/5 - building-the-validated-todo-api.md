# 05 - Building the Validated Todo API

> Day 5 – Validation & Error Handling

In this guide, we will build the complete validated Todo API step by step.

By the end, our API will:

- Validate all incoming data using Pydantic
- Assign IDs automatically
- Return proper status codes
- Return clear error messages using HTTPException

---

# Step 1: Imports

Start with:

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI()

todos = []
id_counter = 1
```

---

# Understanding the Imports

---

## FastAPI

```python
from fastapi import FastAPI, HTTPException
```

`FastAPI` creates our application.

`HTTPException` lets us return proper error responses.

---

## Pydantic

```python
from pydantic import BaseModel, Field
```

`BaseModel` is the foundation of our validation model.

`Field` lets us add extra rules like minimum length.

---

## Literal

```python
from typing import Literal
```

`Literal` restricts a field to specific allowed values.

---

## id_counter

```python
id_counter = 1
```

We use this to assign IDs automatically.

Every time a todo is created, we use this number as the ID and increase it by one.

This way IDs are always unique.

---

# Step 2: Defining the Todo Model

```python
class Todo(BaseModel):
    title: str = Field(min_length=1)
    checked: bool = False
    priority: Literal["low", "medium", "high"] = "medium"
```

---

# Understanding Each Field

---

## title

```python
title: str = Field(min_length=1)
```

Must be a non-empty string.

An empty title is rejected automatically.

---

## checked

```python
checked: bool = False
```

Must be a boolean.

Defaults to False if not provided.

---

## priority

```python
priority: Literal["low", "medium", "high"] = "medium"
```

Must be exactly one of the three allowed values.

Defaults to medium if not provided.

---

# Why Is id Not in the Model?

The user should not choose their own ID.

The server assigns IDs automatically using `id_counter`.

This prevents duplicate IDs.

---

# Step 3: GET /todos

```python
@app.get("/todos")
def get_todos():
    return todos
```

Returns all todos.

No changes needed here.

---

# Step 4: POST /todos

```python
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
```

---

# Understanding This Step

---

## status_code=201

```python
@app.post("/todos", status_code=201)
```

Returns 201 Created instead of 200 when a todo is successfully created.

---

## todo: Todo

```python
def create_todo(todo: Todo):
```

We replaced `todo: dict` with `todo: Todo`.

Pydantic now validates all incoming data automatically.

---

## global id_counter

```python
global id_counter
```

Because `id_counter` is defined outside the function, we need `global` to modify it from inside.

---

## todo.dict()

```python
new_todo = todo.dict()
```

Converts the Pydantic model into a plain dictionary.

---

## Assigning the ID

```python
new_todo["id"] = id_counter
```

We add the ID to the dictionary after converting it.

The user never provides the ID.

---

## Incrementing the Counter

```python
id_counter += 1
```

The next todo will get the next number.

---

# Example

First todo created:

```json
{
  "id": 1,
  "title": "Learn FastAPI",
  "checked": false,
  "priority": "medium"
}
```

Second todo created:

```json
{
  "id": 2,
  "title": "Buy groceries",
  "checked": false,
  "priority": "high"
}
```

IDs are assigned automatically.

---

# Step 5: GET /todos/{id}

```python
@app.get("/todos/{id}")
def get_todo(id: int):
    for todo in todos:
        if todo["id"] == id:
            return todo

    raise HTTPException(
        status_code=404,
        detail="Todo not found"
    )
```

---

# What Changed?

Before:

```python
return {
    "message": "Todo not found"
}
```

This returned 200 even when the todo did not exist.

After:

```python
raise HTTPException(
    status_code=404,
    detail="Todo not found"
)
```

This returns a proper 404 error.

---

# Step 6: PUT /todos/{id}

```python
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
```

---

# What Changed?

---

## updated_todo: Todo

```python
def update_todo(id: int, updated_todo: Todo):
```

Replaced `dict` with `Todo`.

Pydantic now validates the update body as well.

---

## Accessing Fields

```python
todo["title"] = updated_todo.title
```

With a Pydantic model, we access fields using dot notation:

```python
updated_todo.title
updated_todo.checked
updated_todo.priority
```

Instead of:

```python
updated_todo["title"]
```

---

## 404 on Missing Todo

```python
raise HTTPException(
    status_code=404,
    detail="Todo not found"
)
```

If no todo with that ID exists, we return a proper 404.

---

# Step 7: DELETE /todos/{id}

```python
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
```

---

# What Changed?

Before, a missing todo returned:

```python
return {
    "message": "Todo not found"
}
```

with status 200.

Now it returns a proper 404.

---

# Testing Everything

Use Swagger at:

```text
http://127.0.0.1:8000/docs
```

Recommended testing order:

```text
1. POST a valid todo → expect 201

2. POST with an empty title → expect 422

3. POST with an invalid priority → expect 422

4. GET all todos → expect 200

5. GET a specific todo by ID → expect 200

6. GET a todo with a non-existent ID → expect 404

7. PUT to update a todo → expect 200

8. PUT with invalid data → expect 422

9. DELETE a todo → expect 200

10. DELETE a non-existent todo → expect 404
```

---

# Summary

In this guide, we built a fully validated Todo API.

You learned:

- How to define a Pydantic model
- How to use Field for length validation
- How to use Literal for allowed values
- How to assign IDs automatically using a counter
- How to return 201 on creation
- How to raise HTTPException for 404 errors
- How to use dot notation to access Pydantic model fields
- How validation errors look in Swagger
