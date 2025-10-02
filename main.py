"""
FastAPI Todo List Application
A simple web application to manage todo items with CRUD operations.
Uses SQLite database with SQLAlchemy ORM.
"""

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from pydantic import BaseModel
from typing import List

from fastapi_mcp import FastApiMCP

# Database configuration
DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


# Database model
class TodoDB(Base):
    """SQLAlchemy model for todo items in the database"""
    __tablename__ = "todos"

    todo_id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    completed = Column(Boolean, default=False)


# Create database tables
Base.metadata.create_all(bind=engine)


# Pydantic models for request/response validation
class TodoCreate(BaseModel):
    """Schema for creating a new todo item"""
    content: str


class TodoUpdate(BaseModel):
    """Schema for updating an existing todo item"""
    content: str | None = None
    completed: bool | None = None


class TodoResponse(BaseModel):
    """Schema for todo item response"""
    todo_id: int
    content: str
    completed: bool

    class Config:
        from_attributes = True


# FastAPI app initialization
app = FastAPI(
    title="Todo List API",
    description="A simple API to manage todo items",
    version="1.0.0"
)


# Dependency to get database session
def get_db():
    """Provides a database session for each request"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# API Routes

@app.get("/")
def root():
    """Welcome endpoint"""
    return {"message": "Welcome to the Todo List API! Visit /docs for API documentation."}


@app.get("/todos", response_model=List[TodoResponse], operation_id="get_all_todos")
def get_all_todos(db: Session = Depends(get_db)):
    """Retrieve all todo items from the database"""
    todos = db.query(TodoDB).all()
    return todos


@app.get("/todos/{todo_id}", response_model=TodoResponse, operation_id="get_todo")
def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Retrieve a single todo item by its ID"""
    todo = db.query(TodoDB).filter(TodoDB.todo_id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo


@app.post("/todos", response_model=TodoResponse, status_code=201, operation_id="create_todo")
def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo item"""
    new_todo = TodoDB(content=todo.content, completed=False)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo


@app.put("/todos/{todo_id}", response_model=TodoResponse, operation_id="update_todo")
def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """Update an existing todo item"""
    todo = db.query(TodoDB).filter(TodoDB.todo_id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    # Update fields if provided
    if todo_update.content is not None:
        todo.content = todo_update.content
    if todo_update.completed is not None:
        todo.completed = todo_update.completed

    db.commit()
    db.refresh(todo)
    return todo


@app.delete("/todos/{todo_id}", status_code=204, operation_id="delete_todo")
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo item by its ID"""
    todo = db.query(TodoDB).filter(TodoDB.todo_id == todo_id).first()
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return None

# if __name__ == "__main__":
#     import uvicorn

# Expose selected routes via MCP for LLM compatibility
mcp = FastApiMCP(app, include_operations=[
    "get_all_todos",
    "get_todo",
    "create_todo",
    "update_todo",
    "delete_todo"
])
mcp.mount()

    # uvicorn.run(app, host="127.0.0.1", port=8000)
