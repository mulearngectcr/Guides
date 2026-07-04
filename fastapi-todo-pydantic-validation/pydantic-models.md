# 03 - Pydantic Models

> Day 5 – Validation & Error Handling

---

# Introduction

In the previous task, our POST endpoint accepted raw dictionaries:

```python
@app.post("/todos")
def create_todo(todo: dict):
```

This meant the user could send anything.

Pydantic lets us define exactly what the data must look like.

---

# What Is Pydantic?

Pydantic is a Python library for data validation.

It is already installed when you install FastAPI.

FastAPI uses Pydantic internally for all its data handling.

---

# How Does Pydantic Work?

We define a class that describes the shape of our data.

```python
from pydantic import BaseModel

class Todo(BaseModel):
    title: str
    checked: bool
    priority: str
```

When a user sends data to our API, Pydantic checks:

- Is title actually a string?
- Is checked actually a boolean?
- Is priority actually a string?

If anything is wrong, Pydantic automatically rejects the request.

---

# What Is BaseModel?

`BaseModel` is a class provided by Pydantic.

```python
class Todo(BaseModel):
```

By writing `BaseModel` inside the brackets, our `Todo` class inherits Pydantic's validation powers.

Think of it like this:

> Pydantic gives us a smart template. We fill in what fields we need.

You do not need to understand how inheritance works deeply right now.

Just remember:

> Always write `BaseModel` when creating a Pydantic model.

---

# Defining Fields

Inside the class, we define fields using type hints.

```python
class Todo(BaseModel):
    title: str
    checked: bool
    priority: str
```

Each line is a field.

Each field has a name and a type.

---

# Using the Model in FastAPI

Replace `todo: dict` with `todo: Todo`:

```python
@app.post("/todos")
def create_todo(todo: Todo):
    todos.append(todo.dict())
    return {
        "message": "Todo added successfully"
    }
```

Now FastAPI will:

1. Read the incoming JSON
2. Try to create a `Todo` object from it
3. If the data is invalid, automatically return an error
4. If the data is valid, pass it to our function

---

# Understanding todo.dict()

Pydantic models are not plain dictionaries.

To store them in our list, we convert them:

```python
todo.dict()
```

This converts the Pydantic model into a regular Python dictionary.

---

# Example: Valid Request

User sends:

```json
{
  "title": "Learn FastAPI",
  "checked": false,
  "priority": "medium"
}
```

Pydantic checks everything.

All types are correct.

The todo is created.

Response:

```json
{
  "message": "Todo added successfully"
}
```

---

# Example: Invalid Request

User sends:

```json
{
  "title": 12345,
  "checked": "yes",
  "priority": "medium"
}
```

Pydantic immediately rejects it.

Response:

```json
{
  "detail": [
    {
      "msg": "str type expected",
      "loc": ["body", "title"]
    }
  ]
}
```

FastAPI tells the user exactly what went wrong.

We did not write any of this error handling ourselves.

Pydantic did it automatically.

---

# Default Values in Pydantic

We can set default values for optional fields.

```python
class Todo(BaseModel):
    title: str
    checked: bool = False
    priority: str = "medium"
```

Now if the user does not send `checked`, it defaults to `False`.

If the user does not send `priority`, it defaults to `"medium"`.

---

# Validating Priority Values

Currently, `priority` is just a string.

The user could send:

```json
{
  "priority": "ultra urgent"
}
```

We only want to allow:

```text
low
medium
high
```

We can use Python's `Literal` type for this:

```python
from typing import Literal

class Todo(BaseModel):
    title: str
    checked: bool = False
    priority: Literal["low", "medium", "high"] = "medium"
```

Now if the user sends anything else:

```json
{
  "priority": "ultra"
}
```

Pydantic automatically rejects it.

---

# What Is Literal?

`Literal` means:

> This value must be exactly one of these options.

```python
Literal["low", "medium", "high"]
```

Means the only valid values are:

```text
low
medium
high
```

---

# Validating Title Length

We can also ensure title is not empty.

Using Pydantic's `Field`:

```python
from pydantic import BaseModel, Field

class Todo(BaseModel):
    title: str = Field(min_length=1)
    checked: bool = False
    priority: Literal["low", "medium", "high"] = "medium"
```

Now an empty title:

```json
{
  "title": ""
}
```

is automatically rejected.

---

# Our Complete Todo Model

```python
from pydantic import BaseModel, Field
from typing import Literal

class Todo(BaseModel):
    title: str = Field(min_length=1)
    checked: bool = False
    priority: Literal["low", "medium", "high"] = "medium"
```

This enforces:

- `title` must be a non-empty string
- `checked` must be a boolean, defaults to False
- `priority` must be low, medium, or high, defaults to medium

---

# What About id?

Notice we did not include `id` in the model.

That is intentional.

The user should not decide the ID.

The server should assign IDs automatically.

We will handle this in the building guide.

---

# Pydantic and Swagger

Once you use a Pydantic model, Swagger automatically shows the expected fields and types.

Open:

```text
http://127.0.0.1:8000/docs
```

You will see the model schema displayed automatically.

---

# Summary

By now, you should understand:

- What Pydantic is
- What BaseModel is and why we use it
- How to define fields in a Pydantic model
- How Pydantic rejects invalid data automatically
- How default values work in Pydantic
- How to restrict values using Literal
- How to validate field length using Field
- Why we exclude id from the request model

In the next guide, we will learn about **HTTP status codes and error handling**.
