# 06 - Understanding Uvicorn

> Day 1 – Environment Setup & Your First API Endpoint

---

# Introduction

In the previous guide, we learned that FastAPI helps us build APIs.

However, writing FastAPI code alone is not enough.

Consider this application:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Hello World"
    }
```

If you simply execute:

```bash
python main.py
```

nothing useful happens.

The program starts and immediately exits.

Why?

Because FastAPI is **not a web server**.

Something else must:

- Listen for incoming HTTP requests
- Execute your FastAPI code
- Send responses back to users

That is where **Uvicorn** comes in.

---

# What Is a Web Server?

A web server is a program that waits for requests from users and sends back responses.

For example:

```text
Browser
   ↓
Request
   ↓
Web Server
   ↓
Response
   ↓
Browser
```

Without a web server, users cannot communicate with your application.

---

# Real-World Analogy

Imagine a restaurant.

The chef prepares food.

The customers want food.

But customers cannot directly enter the kitchen.

Someone must:

- Accept orders
- Deliver them to the chef
- Bring back the food

That person is the waiter.

```text
Customer
   ↓
Waiter
   ↓
Chef
```

In our application:

```text
User
   ↓
Uvicorn
   ↓
FastAPI
```

FastAPI writes the business logic.

Uvicorn delivers requests and responses.

---

# What Is Uvicorn?

Uvicorn is an **ASGI web server** for Python.

It is responsible for:

- Listening on network ports
- Receiving HTTP requests
- Executing FastAPI code
- Returning responses to clients

Without Uvicorn, your FastAPI application cannot be accessed through a browser.

---

# Installing Uvicorn

Most FastAPI projects install both packages together:

```bash
pip install fastapi uvicorn
```

FastAPI provides the API framework.

Uvicorn provides the web server.

---

# What Does Uvicorn Actually Do?

Suppose your server is running.

A browser requests:

```text
http://127.0.0.1:8000/
```

The process looks like this:

```text
Browser
   ↓
HTTP Request
   ↓
Uvicorn
   ↓
FastAPI Route
   ↓
Python Function
   ↓
JSON Response
   ↓
Uvicorn
   ↓
Browser
```

Uvicorn acts as the communication layer between the internet and your Python code.

---

# Running a FastAPI Application

The standard command is:

```bash
uvicorn main:app --reload
```

This is probably the most common FastAPI command you will use.

Let's understand every part.

---

# Understanding `uvicorn`

The first part:

```bash
uvicorn
```

means:

> Start the Uvicorn web server.

---

# Understanding `main:app`

The second part:

```bash
main:app
```

contains two pieces of information.

---

## `main`

```text
main
```

refers to:

```text
main.py
```

The filename, without the `.py` extension.

---

## `app`

```text
app
```

refers to:

```python
app = FastAPI()
```

the FastAPI application object.

---

# Visual Representation

Suppose we have:

```text
project/
│
└── main.py
```

Inside:

```python
from fastapi import FastAPI

app = FastAPI()
```

Then:

```bash
uvicorn main:app
```

means:

```text
Load:

main.py
   ↓
Find:

app = FastAPI()
   ↓
Run the application
```

---

# Understanding `--reload`

The last part:

```bash
--reload
```

enables automatic reloading.

This means:

> Restart the server whenever your code changes.

---

# Without `--reload`

Imagine you change:

```python
return {
    "message": "Hello World"
}
```

to:

```python
return {
    "message": "FastAPI is awesome"
}
```

Without reload:

```text
Edit Code
   ↓
Stop Server
   ↓
Restart Server
   ↓
Test Again
```

This becomes annoying very quickly.

---

# With `--reload`

Using:

```bash
uvicorn main:app --reload
```

gives:

```text
Edit Code
   ↓
Automatic Restart
   ↓
Refresh Browser
```

Much easier.

---

# Development vs Production

The `--reload` option is only for development.

Why?

Because Uvicorn constantly watches your files for changes.

That consumes additional system resources.

---

## Development

Use:

```bash
uvicorn main:app --reload
```

Benefits:

- Automatic restarts
- Faster development
- Easier debugging

---

## Production

Use:

```bash
uvicorn main:app
```

Benefits:

- Better performance
- Lower memory usage
- Greater stability

Production servers typically use additional tools such as:

- Gunicorn
- Nginx
- Docker
- Kubernetes

These topics will come later in the sprint.

---

# What Happens Internally?

When you start Uvicorn:

```bash
uvicorn main:app
```

the following happens:

---

## Step 1

Uvicorn loads:

```text
main.py
```

---

## Step 2

It searches for:

```python
app = FastAPI()
```

---

## Step 3

It opens a network port.

By default:

```text
127.0.0.1:8000
```

---

## Step 4

It waits for incoming HTTP requests.

---

## Step 5

When a request arrives:

```http
GET /
```

Uvicorn sends it to FastAPI.

---

## Step 6

FastAPI executes:

```python
def home():
```

---

## Step 7

The Python dictionary:

```python
{
    "message": "Hello"
}
```

becomes:

```json
{
  "message": "Hello"
}
```

---

## Step 8

Uvicorn returns the response to the browser.

The entire cycle happens in milliseconds.

---

# Understanding Host and Port

When Uvicorn starts, you might see:

```text
Uvicorn running on http://127.0.0.1:8000
```

Let's understand this.

---

# What Is a Host?

The host identifies where the server runs.

By default:

```text
127.0.0.1
```

means:

> Your own computer.

It is also called:

```text
localhost
```

Both mean the same thing.

---

# What Is a Port?

A port is like a doorway into a program.

Different applications use different ports.

Examples:

| Service             | Common Port |
| ------------------- | ----------- |
| HTTP                | 80          |
| HTTPS               | 443         |
| FastAPI Development | 8000        |
| MySQL               | 3306        |
| PostgreSQL          | 5432        |

Uvicorn uses:

```text
8000
```

by default.

---

# Changing the Port

You can choose a different port:

```bash
uvicorn main:app --port 5000
```

The application becomes available at:

```text
http://127.0.0.1:5000
```

---

# Changing the Host

By default:

```text
127.0.0.1
```

only allows connections from your own computer.

If you want other devices on your network to access the server:

```bash
uvicorn main:app --host 0.0.0.0
```

This tells Uvicorn:

> Accept connections from anywhere.

This is useful during deployment and testing.

---

# Understanding ASGI

Earlier, we said that Uvicorn is an ASGI server.

But what does that mean?

---

# What Is ASGI?

ASGI stands for:

> Asynchronous Server Gateway Interface

It is a standard that defines how web servers communicate with Python applications.

---

# Before ASGI: WSGI

Older frameworks like Flask primarily use:

> WSGI

which stands for:

> Web Server Gateway Interface

WSGI works well for traditional web applications but struggles with modern asynchronous workloads.

---

# Why Was ASGI Created?

Modern applications often need:

- WebSockets
- Live chats
- Streaming
- Real-time notifications
- Long-running AI tasks

ASGI supports these features more effectively.

---

# FastAPI and ASGI

FastAPI was designed specifically for ASGI.

This allows it to support:

```python
async def
```

functions efficiently.

That is one reason FastAPI achieves high performance.

---

# Uvicorn + FastAPI

Together:

```text
FastAPI
   ↓
ASGI Application
   ↓
Uvicorn
   ↓
Internet
```

Uvicorn understands ASGI and knows how to run FastAPI applications.

---

# Common Uvicorn Commands

---

## Basic Server

```bash
uvicorn main:app
```

---

## Development Server

```bash
uvicorn main:app --reload
```

---

## Custom Port

```bash
uvicorn main:app --port 5000
```

---

## Custom Host

```bash
uvicorn main:app --host 0.0.0.0
```

---

## Custom Host and Port

```bash
uvicorn main:app --host 0.0.0.0 --port 8080
```

---

# Real-World Example

Suppose your project looks like:

```text
hello-api/
│
├── venv/
├── main.py
├── requirements.txt
└── .gitignore
```

The workflow becomes:

---

Activate your environment:

```bash
venv\Scripts\activate
```

---

Install dependencies:

```bash
pip install fastapi uvicorn
```

---

Start the server:

```bash
uvicorn main:app --reload
```

---

Visit:

```text
http://127.0.0.1:8000
```

Your API is now running.

---

# Summary

By now, you should understand:

- What a web server is
- Why FastAPI alone cannot handle requests
- What Uvicorn does
- The restaurant analogy
- The meaning of `uvicorn main:app --reload`
- Development vs production servers
- Hosts and ports
- WSGI vs ASGI
- Why FastAPI uses ASGI
- Common Uvicorn commands

In the next guide, we will explore **Swagger UI and ReDoc**, two powerful tools that FastAPI generates automatically for documenting and testing APIs.
