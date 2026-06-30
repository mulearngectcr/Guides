
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

