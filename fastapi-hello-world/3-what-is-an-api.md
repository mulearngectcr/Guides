# 03 - What Is an API?

> Day 1 – Environment Setup & Your First API Endpoint

---

# Introduction

Almost every application you use today relies on APIs.

Examples include:

- Instagram
- WhatsApp
- YouTube
- Swiggy
- Amazon
- ChatGPT
- Spotify

Whenever one piece of software communicates with another, an API is often involved.

Before learning FastAPI, it is important to understand what APIs actually are and why they exist.

---

# What Does API Mean?

API stands for:

> **Application Programming Interface**

That sounds complicated, so let's break it down.

- **Application** → A software program
- **Programming** → Writing instructions for computers
- **Interface** → A way for two things to communicate

An API is simply:

> A set of rules that allows two software applications to communicate with each other.

---

# A Real-World Analogy: The Restaurant

Imagine you visit a restaurant.

You want food, but you do not enter the kitchen and cook it yourself.

Instead:

1. You tell the waiter what you want.
2. The waiter takes your request to the kitchen.
3. The chef prepares the food.
4. The waiter brings the food back to you.

The waiter acts as an interface between you and the kitchen.

```text
Customer
   ↓
Waiter (API)
   ↓
Kitchen (Server)
```

In software:

```text
User
   ↓
Frontend App
   ↓
API
   ↓
Backend Server
```

The API is the middleman.

---

# Why Do We Need APIs?

Imagine if mobile apps had direct access to databases.

Problems:

- Security issues
- Users could modify anything
- No validation of data
- Difficult to maintain

Instead:

```text
Mobile App
    ↓
API
    ↓
Database
```

The API controls what can and cannot happen.

It acts as a security layer and communication channel.

---

# Example: Instagram

Suppose you open Instagram and refresh your feed.

The process looks something like this:

```text
Instagram App
      ↓
Request latest posts
      ↓
Instagram API
      ↓
Instagram Database
      ↓
Post data returned
      ↓
Instagram App displays posts
```

The mobile application never talks directly to the database.

Everything goes through APIs.

---

# Example: ChatGPT

When you type:

```text
What is FastAPI?
```

The process is roughly:

```text
Browser/App
      ↓
API Request
      ↓
OpenAI Servers
      ↓
AI Model Generates Response
      ↓
API Response
      ↓
Browser Displays Text
```

Again, APIs handle the communication.

---

# Frontend vs Backend

To understand APIs, we need to understand two important concepts.

---

## Frontend

The frontend is what users see.

Examples:

- Websites
- Mobile applications
- Desktop applications

Examples of frontend technologies:

- HTML
- CSS
- JavaScript
- React
- Flutter

The frontend focuses on user interaction.

---

## Backend

The backend is responsible for:

- Business logic
- Databases
- Authentication
- Processing requests
- Storing information

Examples:

- Python
- FastAPI
- Node.js
- Java
- Go

Users usually never see the backend directly.

---

# Where Does the API Fit?

The API connects the frontend and backend.

```text
Frontend
    ↓
API
    ↓
Backend
    ↓
Database
```

This allows different systems to communicate in a structured way.

---

# The Client-Server Model

Modern applications typically follow the client-server model.

---

## What Is a Client?

A client is something that requests information.

Examples:

- Mobile apps
- Browsers
- Desktop software
- Smart TVs

---

## What Is a Server?

A server provides information or services.

Examples:

- Web servers
- Database servers
- Authentication servers

---

## Visual Representation

```text
Client
   ↓ Request
Server
   ↓ Response
Client
```

This process is called the **request-response cycle**.

---

# Understanding Requests

A request asks the server to do something.

Examples:

```text
Get my profile
Get today's weather
Show recent messages
Create a new order
Delete this post
```

The client sends these requests through APIs.

---

# Understanding Responses

The server processes the request and returns a response.

Example:

Request:

```text
Get user profile
```

Response:

```json
{
  "id": 1,
  "name": "Alice",
  "age": 22
}
```

Most modern APIs communicate using JSON.

---

# What Is JSON?

JSON stands for:

> JavaScript Object Notation

Despite the name, almost every programming language uses JSON.

JSON is a lightweight format for exchanging data.

---

# Example JSON

```json
{
  "name": "John",
  "age": 20,
  "city": "Kochi"
}
```

---

# Understanding JSON Structure

JSON consists of:

## Keys

```json
"name"
```

Keys describe what the data means.

---

## Values

```json
"John"
```

Values store the actual information.

---

# Multiple Values

```json
{
  "name": "John",
  "age": 20,
  "student": true
}
```

JSON supports:

- Strings
- Numbers
- Booleans
- Lists
- Nested objects

---

# Lists in JSON

Example:

```json
{
  "skills": ["Python", "FastAPI", "Git"]
}
```

---

# Nested JSON

Example:

```json
{
  "user": {
    "name": "John",
    "age": 20
  }
}
```

Modern APIs heavily rely on JSON because it is simple and human-readable.

---

# Real-World API Examples

---

## Weather Application

```text
Weather App
    ↓
Weather API
    ↓
Weather Database
```

The response might look like:

```json
{
  "city": "Kochi",
  "temperature": 29,
  "condition": "Cloudy"
}
```

---

## Food Delivery App

```text
Swiggy App
    ↓
Restaurant API
    ↓
Restaurant Database
```

Response:

```json
{
  "restaurant": "Burger House",
  "rating": 4.5
}
```

---

## Online Shopping

```text
Amazon Website
    ↓
Product API
    ↓
Inventory Database
```

Response:

```json
{
  "product": "Laptop",
  "price": 55000
}
```

---

# Public APIs

Some companies allow developers to use their APIs.

Examples:

- GitHub API
- OpenWeather API
- Spotify API
- OpenAI API

Developers can build applications on top of these services.

For example:

```text
Your App
    ↓
Spotify API
    ↓
Spotify Servers
```

Your application does not need to store millions of songs.

Spotify already provides that functionality.

---

# APIs Enable Software Reuse

Imagine building Google Maps from scratch.

You would need:

- Satellites
- Roads
- Navigation systems
- Traffic analysis

Instead, developers use:

```text
Google Maps API
```

APIs allow developers to reuse existing services.

This greatly speeds up software development.

---

# Why Are APIs Important?

Modern software depends on APIs because they provide:

---

## Separation of Responsibilities

Frontend and backend teams can work independently.

---

## Security

Users never directly access databases.

---

## Reusability

One backend can serve:

- Mobile apps
- Websites
- Desktop applications

simultaneously.

---

## Scalability

Different components can be upgraded independently.

---

## Integration

Different companies can work together using APIs.

---

# The Big Picture

Most modern applications follow this structure:

```text
User
   ↓
Frontend
   ↓
API
   ↓
Backend
   ↓
Database
```

FastAPI helps us build the API layer.

That is exactly what we will learn in this sprint.

---

# Summary

By now, you should understand:

- What API stands for
- Why APIs exist
- The restaurant analogy
- Frontend vs backend
- Client-server architecture
- Requests and responses
- JSON fundamentals
- Real-world examples of APIs
- Why modern software depends on APIs

In the next guide, we will explore **REST APIs**, the most common style of API development used across the industry.
