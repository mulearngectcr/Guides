# 08 - Day 1 Solution: Building Your First FastAPI Application

> Day 1 – Environment Setup & Your First API Endpoint

---

# Objective

The goal of today's task is to:

- Create an isolated Python environment using `venv`
- Install FastAPI and Uvicorn
- Build a simple Hello World API
- Run the server locally
- Explore Swagger UI and ReDoc
- Generate a `requirements.txt` file
- Keep the virtual environment out of Git

By the end of this guide, you will have a complete working FastAPI project.

---

# Final Project Structure

After completing everything, your project should look like this:

```text
hello-api/
│
├── venv/
├── main.py
├── requirements.txt
└── .gitignore
```

Remember:

```text
venv/
```

should never be uploaded to GitHub.

---

# Step 1: Create a Project Folder

Create a new folder for your project.

Example:

```text
hello-api
```

Open your terminal inside that folder.

---

# Step 2: Create a Virtual Environment

Run:

```bash
python -m venv venv
```

---

## Breaking Down the Command

```bash
python -m venv venv
```

---

### `python`

Runs the Python interpreter.

---

### `-m`

Tells Python:

> Run a module as a script.

---

### First `venv`

Uses Python's built-in virtual environment module.

---

### Second `venv`

The name of the folder that will be created.

---

After running the command:

```text
hello-api/
│
└── venv/
```

---

# Step 3: Activate the Virtual Environment

---

## Windows (Command Prompt)

```bash
venv\Scripts\activate
```

---

## Windows (PowerShell)

```powershell
.\venv\Scripts\Activate.ps1
```

---

## Linux/macOS

```bash
source venv/bin/activate
```

---

# Confirm That It Is Active

Your terminal should now look similar to:

```text
(venv) C:\Users\YourName\hello-api>
```

The `(venv)` prefix means the virtual environment is active.

Any packages installed now will remain inside this project.

---

# Step 4: Install FastAPI and Uvicorn

Run:

```bash
pip install fastapi uvicorn
```

---

# What Happens Internally?

`pip` contacts PyPI, downloads:

- FastAPI
- Uvicorn
- Starlette
- Pydantic
- Other required dependencies

and installs everything inside:

```text
venv/
```

instead of your global Python installation.

---

# Step 5: Create `main.py`

Create a file:

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
        "message": "Hello from my API"
    }
```

---

# Understanding the Code

---

## Import FastAPI

```python
from fastapi import FastAPI
```

Imports the FastAPI framework.

---

## Create the Application

```python
app = FastAPI()
```

Creates the main application object.

Every FastAPI project needs one.

---

## Create a Route

```python
@app.get("/")
```

This means:

```http
GET /
```

should execute the function below it.

---

## The Function

```python
def home():
```

This runs whenever someone visits:

```text
http://127.0.0.1:8000
```

---

## Returning a Dictionary

```python
return {
    "message": "Hello from my API"
}
```

FastAPI automatically converts Python dictionaries into JSON.

The browser receives:

```json
{
  "message": "Hello from my API"
}
```

---

# Step 6: Run the Server

Start Uvicorn:

```bash
uvicorn main:app --reload
```

---

# Understanding the Command

```bash
uvicorn main:app --reload
```

---

## `uvicorn`

Starts the Uvicorn web server.

---

## `main`

Refers to:

```text
main.py
```

---

## `app`

Refers to:

```python
app = FastAPI()
```

---

## `--reload`

Automatically restarts the server whenever your code changes.

This is extremely useful during development.

---

# Expected Output

You should see something similar to:

```text
INFO:     Will watch for changes in these directories
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

This means your server is running successfully.

---

# Step 7: Test the API

Open your browser and visit:

```text
http://127.0.0.1:8000
```

You should see:

```json
{
  "message": "Hello from my API"
}
```

Congratulations!

You have built your first FastAPI endpoint.

---

# Step 8: Explore Swagger UI

Visit:

```text
http://127.0.0.1:8000/docs
```

FastAPI automatically generates interactive documentation.

You should see:

```text
GET /

Try it out
Execute
```

---

# Testing with Swagger

Click:

```text
Try it out
```

Then:

```text
Execute
```

Swagger will send a request to your API and display the response.

---

# Step 9: Explore ReDoc

Visit:

```text
http://127.0.0.1:8000/redoc
```

ReDoc presents the same information in a cleaner, more documentation-focused layout.

Try exploring both interfaces.

---

# Step 10: Generate `requirements.txt`

Once your packages are installed, run:

```bash
pip freeze > requirements.txt
```

---

# What Does This Do?

`pip freeze` prints every installed package and version.

The `>` operator saves that output into:

```text
requirements.txt
```

---

# Example Output

Your file might look something like:

```text
annotated-types==0.7.0
anyio==4.10.0
click==8.2.1
fastapi==0.120.0
h11==0.16.0
idna==3.10
pydantic==2.11.7
starlette==0.48.0
typing_extensions==4.15.0
uvicorn==0.35.0
```

The exact versions may differ.

---

# Why Is `requirements.txt` Important?

Imagine another developer clones your repository.

They can recreate your environment using:

```bash
pip install -r requirements.txt
```

This ensures everyone uses the same package versions.

---

# Step 11: Create a `.gitignore`

Create:

```text
.gitignore
```

Add:

```gitignore
venv/
__pycache__/
*.pyc
```

---

# Why Ignore `venv`?

The virtual environment contains:

- Installed packages
- Platform-specific binaries
- Temporary files

These can always be recreated using:

```bash
pip install -r requirements.txt
```

Uploading them to GitHub wastes storage and causes unnecessary problems.

---

# Bonus Challenge 1: Add an About Endpoint

Modify:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Hello from my API"
    }


@app.get("/about")
def about():
    return {
        "name": "Your Name",
        "bio": "Student learning FastAPI"
    }
```

---

Test:

```text
http://127.0.0.1:8000/about
```

---

# Bonus Challenge 2: Path Parameters

Add:

```python
@app.get("/greet/{name}")
def greet(name: str):
    return {
        "message": f"Hello, {name}!"
    }
```

---

Try:

```text
http://127.0.0.1:8000/greet/Alice
```

Response:

```json
{
  "message": "Hello, Alice!"
}
```

---

Try:

```text
http://127.0.0.1:8000/greet/John
```

Response:

```json
{
  "message": "Hello, John!"
}
```

FastAPI automatically extracts the path parameter and passes it to the function.

---

# Complete Solution

The final `main.py` might look like this:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Hello from my API"
    }


@app.get("/about")
def about():
    return {
        "name": "Your Name",
        "bio": "Student learning FastAPI"
    }


@app.get("/greet/{name}")
def greet(name: str):
    return {
        "message": f"Hello, {name}!"
    }
```

---

# Final Checklist

Before submitting, ensure that:

```text
✓ Created a virtual environment using venv
✓ Activated the environment
✓ Installed FastAPI and Uvicorn
✓ Built a GET / endpoint
✓ Tested the endpoint locally
✓ Explored /docs
✓ Explored /redoc
✓ Generated requirements.txt
✓ Added venv/ to .gitignore
✓ Completed bonus challenges (optional)
```

---

# What You Learned Today

You now understand:

- Virtual environments
- pip and package management
- APIs and REST APIs
- FastAPI basics
- Uvicorn and web servers
- Swagger UI and ReDoc
- JSON responses
- Path parameters
- Requirements files
- Git ignore rules

These concepts form the foundation of modern Python backend development.
