import json
import os

from dotenv import load_dotenv
from fastapi import FastAPI
from groq import Groq
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware


load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      
    allow_credentials=False,  
    allow_methods=["*"],      
    allow_headers=["*"],      
)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

MEMORY_FILE = "memory.json"



class ChatRequest(BaseModel):
    message: str


def load_memory():
    try:
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)


def add_message(role, message):
    memory = load_memory()
    memory.append(
        {
            "role": role,
            "content": message,
        }
    )
    save_memory(memory)



def chat(prompt: str):

    history = load_memory()

    history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=history,
    )

    answer = response.choices[0].message.content

    history.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )

    save_memory(history)

    return answer


@app.get("/")
def home():
    return {"message": "Chatbot API is running!"}


@app.post("/chat")
def chatbot(request: ChatRequest):

    response = chat(request.message)

    return {
        "response": response
    }
