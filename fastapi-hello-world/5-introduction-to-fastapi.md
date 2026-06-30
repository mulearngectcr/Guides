# 05 - Introduction to FastAPI

> Day 1 – Environment Setup & Your First API Endpoint

---

# Introduction

Now that we understand:

- What APIs are
- How REST APIs work
- HTTP methods
- JSON responses
- Client-server communication

we can finally start building our own APIs.

The framework we'll use throughout this sprint is **FastAPI**.

FastAPI has become one of the most popular Python frameworks for modern backend development, especially in AI and machine learning applications.

Before writing code, let's understand what FastAPI actually is and why so many developers use it.

---

# What Is a Framework?

Before understanding FastAPI, we need to understand what a framework is.

A framework is a collection of tools, libraries, and conventions that helps developers build applications faster.

Instead of building everything from scratch, a framework provides ready-made solutions for common problems.

---

## Building Without a Framework

Imagine building a web server entirely from scratch.

You would need to handle:

- HTTP requests
- URLs and routing
- JSON conversion
- Error handling
- Input validation
- Documentation generation
- Authentication
- Database connections

That would require thousands of lines of code.

---

## Building With a Framework

A framework handles most of these problems for you.

Example:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Hello World"}
```

In just a few lines, FastAPI automatically provides:

- An HTTP server interface
- Routing
- JSON responses
- Validation
- API documentation
- Error handling

---

# What Is FastAPI?

FastAPI is a modern Python framework for building APIs.

It was created by Sebastián Ramírez and first released in 2018.

FastAPI focuses on three major goals:

- High performance
- Excellent developer experience
- Strong support for modern Python features

---

# Why Is It Called FastAPI?

The name "FastAPI" comes from two ideas.

---

## Fast to Develop

FastAPI allows developers to write APIs using very little code.

Example:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello():
    return {"message": "Hello"}
```

A working API can be built in seconds.

---

## Fast Performance

FastAPI is also extremely fast at handling requests.

It is built on top of:

- Starlette
- Pydantic
- ASGI

making it one of the fastest Python web frameworks available.

In many benchmarks, FastAPI performs close to languages like Go and Node.js.

---

# What Problems Does FastAPI Solve?

FastAPI automatically handles many tasks that developers would otherwise write manually.

Examples include:

---

## Routing

Instead of manually checking URLs:

```python
if path == "/users":
    ...
```

FastAPI provides decorators:

```python
@app.get("/users")
```

---

## JSON Conversion

Returning a Python dictionary:

```python
return {"name": "Alice"}
```

automatically becomes:

```json
{
  "name": "Alice"
}
```

---

## Input Validation

FastAPI checks whether incoming data has the correct types.

Example:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {"id": user_id}
```

If someone sends:

```text
/users/abc
```

FastAPI automatically returns an error because `"abc"` is not an integer.

---

## Documentation Generation

FastAPI automatically creates:

```text
/docs
/redoc
```

No extra configuration is needed.

---

# FastAPI vs Flask vs Django

Python has many web frameworks.

The three most popular are:

---

## Flask

Flask is lightweight and simple.

Advantages:

- Easy to learn
- Flexible
- Minimal structure

Disadvantages:

- Less automatic validation
- Documentation must be configured manually
- More boilerplate code

---

## Django

Django is a full-stack framework.

It includes:

- Authentication systems
- Admin panels
- ORM support
- Database tools
- Templating engines

Advantages:

- Batteries included
- Excellent for large web applications

Disadvantages:

- Can feel heavy for simple APIs

---

## FastAPI

FastAPI focuses specifically on APIs.

Advantages:

- Very high performance
- Automatic documentation
- Strong type checking
- Built-in validation
- Excellent support for async programming

Because of these features, FastAPI is extremely popular in AI startups and backend services.

---

# Why Is FastAPI Popular in AI?

Many machine learning libraries are written in Python:

- PyTorch
- TensorFlow
- NumPy
- Pandas
- Scikit-learn

FastAPI integrates naturally with them.

Example:

```text
User
   ↓
FastAPI Endpoint
   ↓
Machine Learning Model
   ↓
Prediction
```

This makes it ideal for:

- AI APIs
- Chatbots
- Recommendation systems
- Image recognition services
- RAG applications
- LLM backends

---

# Installing FastAPI

Inside your virtual environment:

```bash
pip install fastapi
```

Most developers also install Uvicorn:

```bash
pip install fastapi uvicorn
```

We'll learn about Uvicorn in the next guide.

---

# Your First FastAPI Application

Create a file called:

```text
main.py
```

Add the following code:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Hello from FastAPI"
    }
```

Let's understand each line.

---

# Importing FastAPI

```python
from fastapi import FastAPI
```

This imports the FastAPI class from the framework.

We need it to create our application.

---

# Creating the Application Object

```python
app = FastAPI()
```

This creates a FastAPI application instance.

Think of it as the central object that manages:

- Routes
- Validation
- Documentation
- Configuration

Every FastAPI project has an application object.

---

# Understanding Routes

A route tells FastAPI:

> When someone visits this URL, execute this function.

Example:

```python
@app.get("/")
```

This means:

```text
GET /
```

should call:

```python
home()
```

---

# Understanding Decorators

The syntax:

```python
@app.get("/")
```

is called a **decorator**.

A decorator modifies the behavior of a function.

In this case, it tells FastAPI:

> Register this function as an API endpoint.

---

# The Home Function

```python
def home():
```

This function runs whenever someone sends:

```http
GET /
```

to our server.

---

# Returning Data

```python
return {
    "message": "Hello from FastAPI"
}
```

FastAPI automatically converts Python dictionaries into JSON responses.

The client receives:

```json
{
  "message": "Hello from FastAPI"
}
```

No manual conversion is necessary.

---

# Understanding Type Hints

One of FastAPI's biggest strengths is its use of type hints.

Example:

```python
@app.get("/square/{number}")
def square(number: int):
    return {
        "result": number * number
    }
```

The annotation:

```python
number: int
```

means:

> The value must be an integer.

---

# Automatic Validation

Suppose someone visits:

```text
/square/5
```

Response:

```json
{
  "result": 25
}
```

Everything works correctly.

---

Now suppose someone visits:

```text
/square/hello
```

FastAPI automatically returns an error because:

```text
hello
```

is not an integer.

This is called **automatic validation**.

Many frameworks require developers to implement this manually.

FastAPI provides it by default.

---

# Understanding Async Support

Modern web applications often perform tasks like:

- Database queries
- API calls
- File uploads
- AI inference

These operations can take time.

FastAPI supports asynchronous programming using:

```python
async def
```

Example:

```python
@app.get("/")
async def home():
    return {
        "message": "Hello"
    }
```

This allows FastAPI to handle many requests efficiently.

For Day 1, normal functions are perfectly fine.

We will explore asynchronous programming later in the sprint.

---

# Automatic Documentation

One of FastAPI's most impressive features is automatic documentation generation.

When your server runs, FastAPI creates:

---

## Swagger UI

```text
http://127.0.0.1:8000/docs
```

Features:

- Interactive testing
- Request examples
- Response examples
- Parameter information

---

## ReDoc

```text
http://127.0.0.1:8000/redoc
```

Features:

- Cleaner interface
- Better reading experience
- Professional API documentation

We will explore these tools in more detail later.

---

# Real-World Applications of FastAPI

FastAPI is commonly used for:

---

## AI Services

Examples:

- Chatbots
- LLM backends
- Recommendation systems
- Image classification APIs

---

## Microservices

Large applications are often divided into smaller services.

FastAPI is ideal for building these independent components.

---

## Internal Company Tools

Organizations use FastAPI to build:

- Dashboards
- Analytics systems
- Automation tools

---

## Mobile Application Backends

FastAPI can provide APIs for:

- Android apps
- iOS apps
- Web applications

---

# Why Many Developers Choose FastAPI

FastAPI combines:

- Simplicity
- Performance
- Validation
- Documentation
- Modern Python features

This makes it an excellent choice for beginners and professionals alike.

---

# Summary

By now, you should understand:

- What frameworks are
- Why frameworks exist
- What FastAPI is
- How FastAPI compares with Flask and Django
- Why FastAPI is popular in AI development
- The basics of routes and decorators
- Automatic JSON conversion
- Type hints and validation
- Async support
- Automatic documentation generation

In the next guide, we will learn about **Uvicorn**, the server responsible for running FastAPI applications and handling incoming HTTP requests.
