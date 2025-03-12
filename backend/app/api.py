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

@app.post('/todo', tags=['todos'])
async def create_todo(todo: dict) -> dict:
    todos.append(todo)
    return {'data': todo}

@app.put("/todo/{id}", tags=["todos"])
async def update_todo(id: int, body: dict) -> dict:
    for todo in todos:
        if int(todo["id"]) == id:
            todo["item"] = body["item"]
            return {
                "data": f"Todo with id {id} has been updated."
            }

    return {
        "data": f"Todo with id {id} not found."
    }
