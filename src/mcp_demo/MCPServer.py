import datetime
import json
import uuid
import threading
from pathlib import Path
from time import timezone
from fastmcp import FastMCP
from pydantic import BaseModel
from typing import Literal, Annotated
from fastmcp.exceptions import ToolError

mcp= FastMCP(
  name="Todo",
  instructions= (
    "A simple todo manager. use create_todo, list_todos, get_todo, "
    "update_todo and delete_todo to manage your todos"
  )
)

Status= Literal("Complete", "Pending", "Deleted")

STORE_PATH= Path(__file__).with_name("todos.json")  #local file to store todos

_lock= threading.Lock()  # Lock to synchronise the access to the store

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


@mcp.tool
def create_todo(
    title: Annotated[str, "Short title of todos"],
    description: Annotated[str, "Optional long description"]= "",
    Status: Annotated[Literal["Complete", "Pending", "Deleted"], "pending, completed, deleted"]= "pending",
) -> Todo | None:
  """Create a todo and return"""

  title= title.strip()

  if not title:
    raise ToolError("Title cannot be empty")
  
  now= _now()
  todo= Todo(
    id=uuid.uuid4().hex[:8],
    title= title,
    description= description[:100],
    status=Status,
    created_at=now(),
    updated_at=now()
  )
  with _lock:  # We acquire the lock to pretent concurrent access to store 
    todos= _load()
    todos[todo.id]= todo
    _save(todos)
  
  # We release the lock after we have save the todos
  return todo

@mcp.tool
def list_todo(
    status= Annotated[Status | None, "Complete, pending, deleted or None to list all"]= None
) -> list[Todo]:
  """List todos newly first. Optinoally filter by status"""

  with _lock:
    todos= list[Todo](_load().values())

    if status is not None:
      todos= [todo for todo in todos if todo.status== status]
      todos.sort(key= lambda todo: todo.created_at, reverse=True)

      return todos
    
@mcp.tool
def get_todo(
  todo_id: Annotated[str, "Todo id to get todo"]
) -> Todo | None:
  """Get todo by id"""

  with _lock:
    _, todo= _get_or_raise(todo_id)

    return todo
  
@mcp.tool
def delete_todo(
  todo_id: Annotated[str, "The id to delete todo"]
) -> str:
  """Delete the todo by id and return the id"""

  with _lock:
   todos, todo= _get_or_raise(todo_id)
   del todos[todo_id]
   _save(todos)

  return f"Deleted todo of {todo_id}"








