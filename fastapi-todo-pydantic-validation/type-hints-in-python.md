# 02 - Type Hints in Python

> Day 5 – Validation & Error Handling

---

# Introduction

Before we learn Pydantic, we need to understand something called **type hints**.

Type hints are the foundation that Pydantic is built on.

Without understanding type hints, Pydantic will feel confusing.

---

# What Are Types?

In Python, every value has a type.

For example:

```python
"Learn FastAPI"
```

This is a string.

---

```python
42
```

This is an integer.

---

```python
True
```

This is a boolean.

---

```python
3.14
```

This is a float.

---

# What Are Type Hints?

Type hints allow us to declare what type a variable should be.

For example:

```python
name: str = "Alice"
age: int = 20
is_active: bool = True
```

Here:

- `name` should be a string
- `age` should be an integer
- `is_active` should be a boolean

---

# Type Hints in Functions

We can also use type hints in function parameters.

```python
def greet(name: str):
    return "Hello " + name
```

This tells us:

> The name parameter should be a string.

---

# Return Type Hints

We can also hint what a function returns.

```python
def add(a: int, b: int) -> int:
    return a + b
```

This means:

> This function takes two integers and returns an integer.

---

# Common Types

The most common types you will use:

| Type   | Example Value     | Meaning           |
| ------ | ----------------- | ----------------- |
| `str`  | `"hello"`         | Text              |
| `int`  | `42`              | Whole number      |
| `bool` | `True` or `False` | True or False     |
| `float`| `3.14`            | Decimal number    |

---

# Does Python Enforce Type Hints?

No.

Type hints in plain Python are just hints.

Python does not enforce them at runtime.

For example:

```python
def greet(name: str):
    return "Hello " + name

greet(123)
```

Python runs this without complaining.

---

# So Why Do We Use Them?

Type hints help:

- Editors give better autocomplete suggestions
- Code becomes easier to read and understand
- Tools like Pydantic can enforce them at runtime

This is exactly what Pydantic does.

Pydantic reads your type hints and enforces them.

---

# Type Hints for Our Todo

Let us think about what our todo should look like:

```python
id: int
title: str
checked: bool
priority: str
```

In plain English:

- `id` must be a whole number
- `title` must be text
- `checked` must be true or false
- `priority` must be text

This is exactly what we will pass to Pydantic.

---

# Default Values

Sometimes a field is optional.

We can give it a default value:

```python
checked: bool = False
```

This means:

> If the user does not send checked, use False by default.

---

# Real-World Example

Imagine a sign-up form:

```python
def register(
    username: str,
    age: int,
    is_admin: bool = False
):
```

- `username` is required, must be a string
- `age` is required, must be an integer
- `is_admin` is optional, defaults to False

---

# Summary

By now, you should understand:

- What types are in Python
- What type hints are
- How to use type hints in variables and functions
- Common types: str, int, bool, float
- That Python does not enforce type hints by default
- That Pydantic uses type hints to enforce data at runtime
- How default values work

In the next guide, we will learn how **Pydantic** uses type hints to validate incoming API data automatically.
