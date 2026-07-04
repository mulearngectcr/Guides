# 04 - HTTP Status Codes & Error Handling

> Day 5 – Validation & Error Handling

---

# Introduction

In our current API, when a todo is not found, we return:

```json
{
  "message": "Todo not found"
}
```

The problem:

This response has an HTTP status code of 200.

200 means:

> Everything went fine.

But clearly, something went wrong.

The todo was not found.

This is misleading.

---

# What Are HTTP Status Codes?

Every HTTP response carries a status code.

It is a three-digit number that tells the client what happened.

For example:

```text
200 → Everything is fine
201 → Something was created
400 → The request was wrong
404 → The thing you asked for was not found
422 → Validation failed
500 → The server made a mistake
```

---

# Why Do Status Codes Matter?

Status codes give instant meaning to responses.

When a developer sees:

```text
404
```

they immediately know:

> The resource was not found.

When they see:

```text
201
```

they know:

> Something was successfully created.

This is a universal language that all APIs follow.

---

# Real-World Example: Browser

When you visit a website that does not exist, your browser shows:

```text
404 Not Found
```

The server sent status code 404.

The browser understood it and showed you the error page.

---

# Real-World Example: Instagram

When you try to visit a deleted post:

```text
https://instagram.com/p/deleted-post
```

Instagram returns a 404 response.

---

# The Most Common Status Codes

---

## 200 OK

Everything went fine.

Example: fetching all todos successfully.

```http
GET /todos → 200 OK
```

---

## 201 Created

A new resource was created.

Example: creating a new todo.

```http
POST /todos → 201 Created
```

---

## 400 Bad Request

The client sent something wrong.

Example: sending an invalid priority value after your own manual check.

```http
POST /todos → 400 Bad Request
```

---

## 404 Not Found

The requested resource does not exist.

Example: asking for a todo that was never created.

```http
GET /todos/999 → 404 Not Found
```

---

## 422 Unprocessable Entity

Validation failed.

This is what Pydantic returns automatically when data types are wrong.

```http
POST /todos → 422 Unprocessable Entity
```

---

## 500 Internal Server Error

Something went wrong on the server side.

This is usually a bug in our code.

```http
GET /todos → 500 Internal Server Error
```

---

# How to Return Status Codes in FastAPI

FastAPI makes this simple.

For a 201 response:

```python
from fastapi import FastAPI

@app.post("/todos", status_code=201)
def create_todo(todo: Todo):
    todos.append(todo.dict())
    return {
        "message": "Todo added successfully"
    }
```

Adding `status_code=201` tells FastAPI to return 201 instead of the default 200.

---

# What Is HTTPException?

For error cases like 404, we use `HTTPException`.

```python
from fastapi import FastAPI, HTTPException

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

# Understanding raise

```python
raise HTTPException(...)
```

`raise` stops the function immediately.

It sends the error response to the client.

The rest of the function does not run.

---

# Understanding HTTPException

```python
HTTPException(
    status_code=404,
    detail="Todo not found"
)
```

`status_code` is the HTTP status code to return.

`detail` is the error message the client receives.

---

# Example Response

When a todo is not found:

```json
{
  "detail": "Todo not found"
}
```

With status code 404.

The client immediately knows:

> The todo does not exist.

---

# Replacing Our Old Approach

Old approach:

```python
return {
    "message": "Todo not found"
}
```

This returns 200 even when something is wrong.

New approach:

```python
raise HTTPException(
    status_code=404,
    detail="Todo not found"
)
```

This returns 404 with a clear error message.

---

# Visualizing Status Codes

```text
GET /todos/1

Todo exists?
│
├── Yes → Return todo → 200 OK
│
└── No  → Raise HTTPException → 404 Not Found
```

---

```text
POST /todos

Data valid?
│
├── Yes → Create todo → 201 Created
│
└── No  → Pydantic rejects → 422 Unprocessable Entity
```

---

# Status Codes in Swagger

Swagger shows status codes automatically.

Open:

```text
http://127.0.0.1:8000/docs
```

After adding proper status codes, Swagger will display:

```text
200 - Successful Response
201 - Created
404 - Not Found
422 - Validation Error
```

under each endpoint.

---

# Summary

By now, you should understand:

- What HTTP status codes are
- Why status codes matter
- The most common status codes: 200, 201, 400, 404, 422, 500
- How to return a custom status code in FastAPI
- What HTTPException is
- How to raise a 404 when a todo is not found
- Why we replace plain message returns with HTTPException

