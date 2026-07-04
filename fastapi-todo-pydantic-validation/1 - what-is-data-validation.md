# 01 - What is Data Validation?

> Day 5 – Validation & Error Handling

---

# Introduction

So far, our Todo API accepts any data the user sends.

For example, if someone sends:

```json
{
  "id": "hello",
  "title": 12345,
  "checked": "maybe",
  "priority": "urgent"
}
```

Our API would accept it without complaint.

This is a problem.

Our API has no idea what good data looks like.

It will store anything — even nonsense.

This is where **data validation** comes in.

---

# What Is Data Validation?

Data validation means checking that the data you receive is correct before using it.

Examples:

- Is the title actually a string?
- Is checked actually true or false?
- Is priority one of the allowed values?

If the data is wrong, we reject it immediately and tell the user what went wrong.

---

# Real-World Example: Google Forms

Imagine filling out a Google Form.

You see a field:

```text
Enter your age
```

You type:

```text
hello
```

Google immediately says:

```text
Please enter a valid number.
```

It does not submit the form.

It validates your input first.

---

# Real-World Example: Instagram Sign Up

When creating an Instagram account, you enter a password.

Instagram checks:

- Is it at least 6 characters?
- Does it contain letters and numbers?

If not:

```text
Password must be at least 6 characters.
```

Instagram is validating your data.

---

# Real-World Example: Booking a Flight

When booking a flight online, you enter your travel date.

If you enter a date in the past:

```text
Please select a future date.
```

The form rejects invalid data immediately.

---

# Why Does Validation Matter?

Without validation, bad data enters your system.

Imagine a bank application.

A user sends:

```json
{
  "amount": "free money please"
}
```

Without validation, this might crash the server.

Or worse, cause unexpected behaviour.

Validation prevents this.

---

# What Happens Without Validation?

Let us look at our current API.

```python
@app.post("/todos")
def create_todo(todo: dict):
    todos.append(todo)
    return {
        "message": "Todo added successfully"
    }
```

If someone sends:

```json
{
  "id": "abc",
  "title": 999,
  "checked": "yes please",
  "priority": "ultra urgent"
}
```

Our API accepts it.

Now our list contains nonsense data.

When someone reads it later, things break in unexpected ways.

---

# What Should Happen Instead?

When someone sends invalid data, the server should:

```text
1. Reject the request immediately

2. Return a clear error message

3. Tell the user exactly what went wrong
```

For example:

```json
{
  "detail": "title must be a string"
}
```

This is much better than silently storing broken data.

---

# Two Types of Problems Validation Solves

---

## Wrong Types

A user sends a number where we expect a string:

```json
{
  "title": 12345
}
```

We expected:

```json
{
  "title": "Learn FastAPI"
}
```

---

## Invalid Values

A user sends a priority we do not recognise:

```json
{
  "priority": "ultra"
}
```

We only accept:

```text
low
medium
high
```

Validation catches both problems.

---

# How Do We Add Validation in FastAPI?

FastAPI uses a library called **Pydantic**.

Pydantic allows us to define exactly what our data should look like.

For example:

```python
class Todo(BaseModel):
    title: str
    checked: bool
    priority: str
```

If the incoming data does not match this definition, Pydantic automatically rejects it.

We will explore Pydantic in the next guide.

---

# Summary

By now, you should understand:

- What data validation is
- Why APIs need validation
- Real-world examples of validation
- What happens without validation
- The two main types of validation problems
- That FastAPI uses Pydantic for validation

In the next guide, we will learn about **type hints in Python**, which is the foundation Pydantic is built on.2  
