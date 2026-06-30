# 02 - Understanding pip & Python Package Management

> Day 1 – Environment Setup & Your First API Endpoint

---

# Introduction

Python is a powerful language, but its real strength comes from its enormous ecosystem of libraries and frameworks.

Instead of writing everything from scratch, developers can use packages created by other programmers.

Examples include:

- FastAPI for building APIs
- NumPy for numerical computing
- Pandas for data analysis
- Requests for making HTTP requests
- PyTorch for machine learning
- OpenCV for computer vision

The tool that makes all of this possible is **pip**.

Understanding pip is essential because almost every Python project uses it.

---

# What Is pip?

`pip` is Python's official package manager.

A package manager is a tool that helps developers:

- Install packages
- Remove packages
- Update packages
- View installed packages
- Manage project dependencies

Without pip, installing software would be extremely difficult.

---

# What Does pip Stand For?

The most common explanation is:

> **Pip Installs Packages**

Although the name was originally recursive:

> **Pip Installs Python**

Today, most developers simply think of pip as Python's package manager.

---

# Why Do We Need pip?

Imagine you want to use FastAPI.

Without pip, you would need to:

1. Visit the FastAPI repository.
2. Download the source code manually.
3. Download every dependency manually.
4. Place everything in the correct folders.
5. Repeat the process whenever updates are released.

That would be extremely inconvenient.

With pip:

```bash
pip install fastapi
```

Everything is downloaded and installed automatically.

---

# What Is a Package?

A package is a collection of Python code that solves a specific problem.

Examples:

| Package  | Purpose                |
| -------- | ---------------------- |
| FastAPI  | Build web APIs         |
| NumPy    | Numerical computations |
| Pandas   | Data analysis          |
| Requests | HTTP requests          |
| OpenCV   | Image processing       |
| PyTorch  | Machine learning       |

Instead of reinventing the wheel, developers reuse these tools.

---

# Where Do Packages Come From?

Most Python packages are downloaded from:

> **PyPI (Python Package Index)**

Website:

https://pypi.org

PyPI is the official repository for Python packages.

It contains millions of libraries created by developers around the world.

When you run:

```bash
pip install fastapi
```

pip contacts PyPI, downloads the package, and installs it.

---

# Installing Your First Package

The general syntax is:

```bash
pip install package_name
```

Example:

```bash
pip install fastapi
```

Installing multiple packages:

```bash
pip install fastapi uvicorn
```

pip automatically installs any additional dependencies required by those packages.

---

# Understanding Dependencies

Suppose you install:

```bash
pip install fastapi
```

FastAPI itself depends on other packages, including:

- Starlette
- Pydantic
- Typing Extensions

pip installs these automatically.

This is called **dependency management**.

---

# Dependency Trees

A package often depends on other packages.

Example:

```text
FastAPI
│
├── Starlette
│
├── Pydantic
│
└── Typing Extensions
```

Installing FastAPI means installing its entire dependency tree.

Doing this manually would be extremely difficult.

pip handles everything for us.

---

# Why Virtual Environments Matter

Suppose you install FastAPI globally:

```bash
pip install fastapi
```

Every project on your computer now shares that installation.

That can create version conflicts.

Instead, we activate a virtual environment first:

```bash
venv\Scripts\activate
```

Then install packages:

```bash
pip install fastapi uvicorn
```

The packages stay inside that specific project.

---

# Viewing Installed Packages

To see all installed packages:

```bash
pip list
```

Example output:

```text
Package           Version
-------------------------
fastapi           0.120.0
pydantic          2.11.7
starlette         0.48.0
uvicorn           0.35.0
```

---

# Viewing Information About a Package

You can inspect a package:

```bash
pip show fastapi
```

Example output:

```text
Name: fastapi
Version: 0.120.0
Author: Sebastián Ramírez
Location: ...
Requires: pydantic, starlette
```

This helps developers understand package dependencies and installation details.

---

# Upgrading Packages

To upgrade a package:

```bash
pip install --upgrade fastapi
```

pip checks for newer versions and installs them.

---

# Uninstalling Packages

To remove a package:

```bash
pip uninstall fastapi
```

pip will ask for confirmation before deleting the files.

---

# What Is `requirements.txt`?

One of the most important files in Python projects is:

```text
requirements.txt
```

It contains a list of all installed packages and their versions.

Example:

```text
fastapi==0.120.0
uvicorn==0.35.0
starlette==0.48.0
pydantic==2.11.7
```

---

# Why Do We Need `requirements.txt`?

Imagine you build an API and upload the code to GitHub.

Another developer clones the repository.

How do they know which packages to install?

The answer is:

```text
requirements.txt
```

It acts as a recipe for recreating your environment.

---

# Generating `requirements.txt`

The command is:

```bash
pip freeze > requirements.txt
```

Let's understand it.

---

## What Does `pip freeze` Do?

```bash
pip freeze
```

prints every installed package and its exact version.

Example:

```text
fastapi==0.120.0
uvicorn==0.35.0
starlette==0.48.0
```

---

## What Does `>` Mean?

The `>` symbol redirects output into a file.

Example:

```bash
pip freeze > requirements.txt
```

means:

> Take the output from `pip freeze` and save it into `requirements.txt`.

---

# Installing Packages from `requirements.txt`

If someone clones your project, they can recreate everything using:

```bash
pip install -r requirements.txt
```

The `-r` flag means:

> Read package names from a file.

pip then installs the exact versions listed.

---

# Real-World Example

Suppose your project structure looks like this:

```text
hello-api/
│
├── main.py
├── requirements.txt
└── .gitignore
```

A new developer can run:

```bash
python -m venv venv
```

Activate it:

```bash
venv\Scripts\activate
```

And install dependencies:

```bash
pip install -r requirements.txt
```

Their environment becomes identical to yours.

This is called **reproducibility**.

---

# Best Practices

Professional Python developers usually follow these rules:

---

## Always Use Virtual Environments

Do not install packages globally unless absolutely necessary.

---

## Generate `requirements.txt`

Always include:

```text
requirements.txt
```

in your repositories.

---

## Pin Versions

Good:

```text
fastapi==0.120.0
```

Bad:

```text
fastapi
```

Version pinning prevents unexpected issues when packages update.

---

## Keep Dependencies Minimal

Install only what your project actually needs.

This keeps environments smaller and easier to maintain.

---

# Common pip Commands

## Install a Package

```bash
pip install fastapi
```

---

## Install Multiple Packages

```bash
pip install fastapi uvicorn
```

---

## List Installed Packages

```bash
pip list
```

---

## Show Package Details

```bash
pip show fastapi
```

---

## Upgrade a Package

```bash
pip install --upgrade fastapi
```

---

## Remove a Package

```bash
pip uninstall fastapi
```

---

## Generate Requirements File

```bash
pip freeze > requirements.txt
```

---

## Install From Requirements

```bash
pip install -r requirements.txt
```

---

# Summary

By now, you should understand:

- What pip is
- Why package managers exist
- What PyPI is
- How packages are installed
- What dependencies are
- How dependency trees work
- Why virtual environments are important
- How to generate `requirements.txt`
- How to recreate environments using `pip install -r`

In the next guide, we will learn what APIs are, how applications communicate with each other, and why web APIs are fundamental to modern software development.
