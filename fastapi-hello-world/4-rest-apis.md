# 04 - Understanding REST APIs

> Day 1 – Environment Setup & Your First API Endpoint

---

# Introduction

In the previous guide, we learned what APIs are and why modern applications depend on them.

However, not all APIs are designed in the same way.

The most popular approach used today is called **REST**.

When people say:

> "I'm building a REST API using FastAPI"

they mean that their API follows a particular set of design principles.

Understanding REST is important because almost every web application, mobile app, and backend service uses it.

---

# What Does REST Mean?

REST stands for:

> **Representational State Transfer**

The term was introduced by computer scientist Roy Fielding in his doctoral dissertation in 2000.

The name sounds complicated, but the basic idea is simple:

> REST is a way of organizing APIs so that they are predictable, consistent, and easy to understand.

---

# The Core Idea Behind REST

REST treats everything as a **resource**.

Examples:

```text
Users
Products
Orders
Posts
Comments
Messages
Videos
```

Each resource has its own URL.

Examples:

```text
/users
/products
/orders
/posts
```

Instead of creating random endpoints, REST organizes everything around resources.

---

# What Is a Resource?

A resource is simply something your application manages.

Examples:

---

## Social Media Platform

Resources:

```text
Users
Posts
Comments
Messages
Stories
```

---

## E-Commerce Website

Resources:

```text
Products
Orders
Customers
Payments
```

---

## Food Delivery Application

Resources:

```text
Restaurants
Menus
Orders
Drivers
Reviews
```

REST APIs are built around these resources.

---

# Understanding Endpoints

An endpoint is a specific URL that represents a resource.

Examples:

```text
/users
/products
/orders
```

You can think of endpoints as addresses for your data.

---

# Example: Users

Suppose we have a user system.

---

## Get All Users

```http
GET /users
```

Response:

```json
[
  {
    "id": 1,
    "name": "Alice"
  },
  {
    "id": 2,
    "name": "Bob"
  }
]
```

---

## Get a Specific User

```http
GET /users/1
```

Response:

```json
{
  "id": 1,
  "name": "Alice"
}
```

The endpoint:

```text
/users/1
```

means:

> Give me the user whose ID is 1.

---

# HTTP Methods

REST APIs use HTTP methods to describe actions.

Instead of writing:

```text
/createUser
/deleteUser
/updateUser
```

REST uses standard HTTP methods.

---

# GET

GET means:

> Retrieve information.

Examples:

```http
GET /users
GET /products
GET /orders
```

GET requests should not modify data.

They only fetch information.

---

# POST

POST means:

> Create something new.

Example:

```http
POST /users
```

Request body:

```json
{
  "name": "Alice"
}
```

Response:

```json
{
  "id": 1,
  "name": "Alice"
}
```

A new user has been created.

---

# PUT

PUT means:

> Replace an entire resource.

Example:

```http
PUT /users/1
```

Request:

```json
{
  "name": "Alice Smith",
  "age": 22
}
```

The entire user record is replaced with the new data.

---

# PATCH

PATCH means:

> Update only specific fields.

Example:

```http
PATCH /users/1
```

Request:

```json
{
  "age": 23
}
```

Only the age changes.

Everything else remains the same.

---

# DELETE

DELETE means:

> Remove a resource.

Example:

```http
DELETE /users/1
```

The user with ID 1 is deleted.

---

# Summary of HTTP Methods

| Method | Purpose                 |
| ------ | ----------------------- |
| GET    | Read data               |
| POST   | Create data             |
| PUT    | Replace data            |
| PATCH  | Update part of the data |
| DELETE | Remove data             |

These are the most common operations in REST APIs.

---

# Why Use Standard Methods?

Imagine if every company invented its own system:

```text
/getUser
/fetchUser
/removeUser
/makeUser
```

Developers would constantly need to learn new conventions.

REST solves this by using universally accepted HTTP methods.

Anyone familiar with REST can understand a new API quickly.

---

# Understanding URLs in REST APIs

REST URLs should describe resources, not actions.

---

## Bad Example

```text
/createProduct
/deleteProduct
/getProduct
```

---

## Good Example

```text
POST /products
DELETE /products/1
GET /products/1
```

The HTTP method describes the action.

The URL describes the resource.

This is one of the core principles of REST.

---

# Path Parameters

Sometimes we need information about a specific resource.

Example:

```http
GET /users/42
```

The number:

```text
42
```

is called a **path parameter**.

It is part of the URL itself.

---

# FastAPI Example

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    return {
        "user_id": user_id
    }
```

If someone visits:

```text
/users/42
```

FastAPI automatically extracts:

```python
user_id = 42
```

---

# Query Parameters

Query parameters provide additional options.

Example:

```text
/products?category=laptops
```

Here:

```text
category=laptops
```

is a query parameter.

---

# Multiple Query Parameters

Example:

```text
/products?category=laptops&page=2&sort=price
```

Meaning:

```text
Category: laptops
Page: 2
Sort by: price
```

Query parameters help filter or customize responses.

---

# Path Parameters vs Query Parameters

---

## Path Parameters

Used to identify a specific resource.

Example:

```text
/users/42
```

Meaning:

```text
Get user number 42
```

---

## Query Parameters

Used to filter or customize data.

Example:

```text
/users?age=20
```

Meaning:

```text
Get users whose age is 20
```

---

# Understanding HTTP Status Codes

When servers respond, they include status codes.

These codes tell clients whether a request succeeded or failed.

---

# 200 OK

```http
200 OK
```

The request succeeded.

Example:

```http
GET /users/1
```

Response:

```json
{
  "id": 1,
  "name": "Alice"
}
```

---

# 201 Created

```http
201 Created
```

A new resource was successfully created.

Example:

```http
POST /users
```

---

# 400 Bad Request

```http
400 Bad Request
```

The client sent invalid data.

Example:

```json
{
  "age": "twenty"
}
```

when the API expects a number.

---

# 401 Unauthorized

```http
401 Unauthorized
```

Authentication is required.

The user needs to log in.

---

# 403 Forbidden

```http
403 Forbidden
```

The user is authenticated but does not have permission.

---

# 404 Not Found

```http
404 Not Found
```

The requested resource does not exist.

Example:

```http
GET /users/9999
```

---

# 500 Internal Server Error

```http
500 Internal Server Error
```

Something went wrong on the server.

Usually, this means a bug in the backend code.

---

# Real-World Example: Instagram

Suppose you open a user's profile.

The request might look like:

```http
GET /users/123
```

Response:

```json
{
  "username": "john_doe",
  "followers": 1200
}
```

---

# Real-World Example: Swiggy

Getting restaurant information:

```http
GET /restaurants/25
```

Response:

```json
{
  "name": "Burger House",
  "rating": 4.5
}
```

---

# Real-World Example: Amazon

Adding an order:

```http
POST /orders
```

Request:

```json
{
  "product_id": 10,
  "quantity": 2
}
```

Response:

```json
{
  "order_id": 500
}
```

---

# REST Best Practices

Professional developers usually follow these guidelines.

---

## Use Nouns, Not Verbs

Bad:

```text
/createUser
/deleteUser
```

Good:

```text
POST /users
DELETE /users/1
```

---

## Use Plural Resource Names

Prefer:

```text
/users
/products
/orders
```

instead of:

```text
/user
/product
/order
```

---

## Keep URLs Simple

Good:

```text
/users/1/posts
```

Bad:

```text
/getAllPostsForSpecificUserById
```

---

## Use Proper Status Codes

Return:

```text
200 OK
201 Created
404 Not Found
```

instead of always returning:

```text
200 OK
```

This makes APIs easier to understand and debug.

---

# Why Is REST So Popular?

REST became popular because it provides:

---

## Simplicity

The rules are easy to understand.

---

## Predictability

Developers know what to expect.

---

## Scalability

Large systems can be built using the same principles.

---

## Language Independence

REST works with:

- Python
- Java
- JavaScript
- Go
- Rust
- C#

Any technology that supports HTTP.

---

# The Big Picture

A typical REST API looks like:

```text
GET    /users
GET    /users/1
POST   /users
PUT    /users/1
PATCH  /users/1
DELETE /users/1
```

The URL represents the resource.

The HTTP method represents the action.

This is the foundation of modern web APIs.

---

# Summary

By now, you should understand:

- What REST means
- What resources are
- What endpoints are
- The five major HTTP methods
- Path parameters
- Query parameters
- Common HTTP status codes
- REST best practices
- Why REST is widely used

In the next guide, we will learn about **FastAPI**, the framework we will use to build our own REST APIs in Python.
