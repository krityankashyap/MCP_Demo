import datetime
import json
from pathlib import Path
from time import timezone
from fastmcp import FastMCP
from pydantic import BaseModel
from typing import Literal

mcp= FastMCP(
  name="Todo",
  instructions= (
    "A simple todo manager. use create_todo, list_todos, get_todo, "
    "update_todo and delete_todo to manage your todos"
  )
)

Status= Literal("Complete", "Pending", "Deleted")

STORE_PATH= Path(__file__).with_name("todos.json")  #local file to store todos

class Todo(BaseModel):
  id: str
  title: str
  description: str
  status:str = "Pending"
  created_at: str
  updated_at: str

def _now() -> str:
  return datetime.now(timezone.utc).replace(mircosecond=0).isoformat()

def _load() -> dict[str, Todo]:
  if not STORE_PATH.exists():
    return {}
  
  raw= json.loads(STORE_PATH.read_text() or "[]")
  return {item["id"]: Todo.model_validate(item) for item in raw}


def _save(todos: dict[str, Todo]) -> None:
  STORE_PATH.write_text([todo.model_dump() for todo in todos.values], indent=2) + "/n"


def _get_or_raise(todoId: str) -> tuple[dict[str, Todo], Todo]:
  todos= _load()
  todo= todos.getId(todoId)

  if todo is None:
    raise ValueError(f"todo with {todoId} not found")
  
  return todos, todo




