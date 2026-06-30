# 01 - Understanding Virtual Environments (`venv`)

> Day 1 – Environment Setup & Your First API Endpoint

---

# Introduction

One of the first things professional Python developers learn is how to use **virtual environments**.

If you've only written small Python programs before, you might have installed packages directly on your computer without thinking much about it.

That works for small experiments, but real projects require a better approach.

Virtual environments solve one of the biggest problems in software development:

> Different projects often need different versions of the same package.

Understanding this concept is essential before building web applications with FastAPI.

---

# What Are Python Packages?

Python comes with many built-in modules:

```python
import math
import random
import os
```

These are part of Python's standard library.

However, real-world applications often need additional functionality:

- Web frameworks like FastAPI
- Data science libraries like NumPy
- Machine learning tools like PyTorch
- Database connectors
- Image processing libraries
- API clients

These external libraries are called **packages**.

Examples:

```bash
pip install fastapi
pip install numpy
pip install pandas
pip install requests
```

---

# The Problem with Global Installation

Suppose you build two different projects.

## Project A

```text
Online Store API
FastAPI Version: 0.100
```

---

## Project B

```text
AI Assistant Backend
FastAPI Version: 0.120
```

If everything is installed globally on your computer, Python can only keep one version installed.

Your system might look like this:

```text
Python
└── Global Packages
    └── FastAPI (Only one version)
```

If Project B upgrades FastAPI, Project A might stop working.

This problem is called a **dependency conflict**.

---

# Real-World Example

Imagine two games:

```text
Game A
Needs DirectX 10

Game B
Needs DirectX 12
```

Installing one version might break the other.

Software developers face similar problems every day.

Virtual environments solve this issue.

---

# What Is a Virtual Environment?

A virtual environment is an isolated Python environment created specifically for one project.

Each project gets:

- Its own Python packages
- Its own dependencies
- Its own versions
- Its own configuration

Nothing affects other projects.

---

# Visualizing a Virtual Environment

Without virtual environments:

```text
Computer
│
└── Python
    ├── FastAPI
    ├── NumPy
    ├── Django
    └── Requests
```

Everything is shared.

---

With virtual environments:

```text
Project A
│
├── venv
│   └── FastAPI 0.100
│

Project B
│
├── venv
│   └── FastAPI 0.120
```

Now both projects can use different versions safely.

---

# What Does `venv` Mean?

`venv` stands for:

> Virtual Environment

Python includes a built-in module called `venv` that allows us to create isolated environments without installing additional software.

---

# Creating a Virtual Environment

Suppose we create a project folder:

```text
hello-api/
```

Move into the folder:

```bash
cd hello-api
```

Then run:

```bash
python -m venv venv
```

This command creates a new virtual environment.

---

# Breaking Down the Command

```bash
python -m venv venv
```

Let's understand every part.

---

## `python`

This runs the Python interpreter.

---

## `-m`

The `-m` flag means:

> Execute a Python module as a script.

Instead of writing:

```python
import venv
```

Python runs the module directly.

---

## First `venv`

The first `venv` refers to Python's built-in virtual environment module.

It tells Python:

> Use the virtual environment tool.

---

## Second `venv`

The second `venv` is simply the name of the folder that will be created.

You could technically write:

```bash
python -m venv my_environment
```

which would create:

```text
my_environment/
```

However, most developers use:

```text
venv/
```

because it is simple and widely recognized.

---

# What Gets Created?

After running the command:

```bash
python -m venv venv
```

your project might look like this:

```text
hello-api/
│
└── venv/
    ├── Include/
    ├── Lib/
    ├── Scripts/
    └── pyvenv.cfg
```

---

# Understanding These Folders

## Include

Contains C header files used by certain packages.

Most beginners never need to touch this.

---

## Lib

Stores all installed Python packages.

When you run:

```bash
pip install fastapi
```

the files are placed here.

---

## Scripts (Windows)

Contains important tools:

```text
activate
activate.bat
pip.exe
python.exe
```

This folder is responsible for activating the environment.

---

## pyvenv.cfg

Stores configuration information about the virtual environment.

It tells Python which base installation created this environment.

---

# Activating the Virtual Environment

Creating a virtual environment is not enough.

You must activate it.

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

## Linux and macOS

```bash
source venv/bin/activate
```

---

# How Do You Know It Worked?

Your terminal changes.

Before:

```text
C:\Users\User\hello-api>
```

After:

```text
(venv) C:\Users\User\hello-api>
```

The `(venv)` prefix indicates that the virtual environment is currently active.

Any packages you install now will remain inside this project.

---

# What Happens Internally?

When activation occurs, Python changes:

```text
PATH
```

so that commands like:

```bash
python
pip
```

point to the versions inside your virtual environment instead of the global installation.

This is why:

```bash
pip install fastapi
```

does not affect other projects.

---

# Installing Packages Inside a Virtual Environment

After activation:

```bash
pip install fastapi uvicorn
```

The packages are installed into:

```text
hello-api/
└── venv/
    └── Lib/
```

instead of your system-wide Python installation.

---

# Deactivating a Virtual Environment

When you're finished working, you can deactivate it:

```bash
deactivate
```

The terminal returns to:

```text
C:\Users\User\hello-api>
```

Your global Python installation becomes active again.

---

# Why Do We Use Virtual Environments?

Professional developers use virtual environments because they provide:

## Isolation

Projects do not interfere with each other.

---

## Reproducibility

Anyone can recreate the same environment using:

```bash
pip install -r requirements.txt
```

---

## Version Management

Different projects can use different package versions safely.

---

## Cleaner Systems

Your global Python installation stays uncluttered.

---

# Why Should `venv` Not Be Uploaded to GitHub?

The virtual environment contains:

- Installed packages
- Temporary files
- Platform-specific binaries

These files can always be recreated.

Therefore, we usually add:

```gitignore
venv/
```

to `.gitignore`.

---

# What Is `.gitignore`?

`.gitignore` tells Git:

> Ignore these files and folders.

Example:

```gitignore
venv/
__pycache__/
*.pyc
```

This prevents unnecessary files from being uploaded to repositories.

---

# Summary

By now, you should understand:

- What Python packages are
- The problem with global installations
- What dependency conflicts are
- What virtual environments solve
- How `python -m venv venv` works
- How to activate and deactivate a virtual environment
- Why `venv/` should not be committed to Git

In the next guide, we will learn about **pip**, Python's package manager, and how it works with virtual environments.
