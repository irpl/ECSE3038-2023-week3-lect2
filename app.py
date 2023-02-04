from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "https://ecse-week3-demo.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

fake_database = []

@app.get("/todos")
async def get_all_todos():
  return fake_database

@app.post("/todos")
async def create_todo(request: Request):
  todo = await request.json()
  fake_database.append(todo)
  return todo

@app.patch("/todos/{id}")
async def change_todo(id: int, request: Request):
  changed_todo = await request.json()
  
  for todo in fake_database:
    if todo["id"] == id:
      index = fake_database.index(todo)
      fake_database[index]["isDone"] = changed_todo["isDone"]
      return fake_database[index]
  raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/todos/{id}")
async def delete_todo(id: int):
  for todo in fake_database:
    if todo["id"] == id:
      fake_database.remove(todo)
      return {"deleted": True}
  raise HTTPException(status_code=404, detail="Item not found")