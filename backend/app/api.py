from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    "http://localhost:5173",
    "localhost:5173"
]

todos = [
    {"id": 1, "item": "Buy groceries"},
    {"id": 2, "item": "Clean the house"},
    {"id": 3, "item": "Complete project"}
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {'"message": "Welcome to your todo list."'}

@app.get('/todo', tags=['todos'])
async def read_todos() -> dict:
    return {"data": todos}
