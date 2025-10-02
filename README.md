# FastAPI MCP Todo App

A simple yet complete Todo List web application built with FastAPI and integrated with Model Context Protocol (MCP) for LLM compatibility.

## Features

- ✅ Full CRUD operations for todo items
- ✅ SQLite database with SQLAlchemy ORM
- ✅ MCP integration for LLM interactions
- ✅ Type hints and validation with Pydantic


## Tech Stack

- **FastAPI** - Modern, fast web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Lightweight database
- **FastAPI-MCP** - Model Context Protocol integration
- **Pydantic** - Data validation
- **Uvicorn** - ASGI server

## Installation

### Using uv (recommended)

```bash
# Clone the repository
git clone https://github.com/suraj-yadav-aiml/fastapi-mcp-todo-app.git
cd fastapi-mcp-todo-app

# Install dependencies
uv pip install -r requirements.txt
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/suraj-yadav-aiml/fastapi-mcp-todo-app.git
cd fastapi-mcp-todo-app

# Install dependencies
pip pip install -r requirements.txt
```

## Usage

### Running the Application

```bash
# Using uvicorn directly
uvicorn main:app --reload

# Or specify host and port
uvicorn main:app --host 0.0.0.0 --port 8000
```

The API will be available at `http://127.0.0.1:8000`

### API Documentation

Once running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| GET | `/todos` | Get all todos |
| GET | `/todos/{todo_id}` | Get a specific todo |
| POST | `/todos` | Create a new todo |
| PUT | `/todos/{todo_id}` | Update a todo |
| DELETE | `/todos/{todo_id}` | Delete a todo |

## Example Requests

### Create a Todo

```bash
curl -X POST "http://127.0.0.1:8000/todos" \
  -H "Content-Type: application/json" \
  -d '{"content": "Learn FastAPI"}'
```

### Get All Todos

```bash
curl "http://127.0.0.1:8000/todos"
```

### Update a Todo

```bash
curl -X PUT "http://127.0.0.1:8000/todos/1" \
  -H "Content-Type: application/json" \
  -d '{"content": "Learn FastAPI and MCP", "completed": true}'
```

### Delete a Todo

```bash
curl -X DELETE "http://127.0.0.1:8000/todos/1"
```

## MCP Integration

This application exposes its API endpoints via MCP, making it compatible with LLM-based tools and agents. The following operations are available through MCP:

- `get_all_todos`
- `get_todo`
- `create_todo`
- `update_todo`
- `delete_todo`

## Deployment

### Deploy to Render

This app is configured for easy deployment to Render using the included `render.yaml` file.

1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service and select this repository
4. Render will automatically detect the `render.yaml` configuration

## Project Structure

```
fastapi-mcp-todo-app/
├── main.py           # Main application file
├── render.yaml       # Render deployment configuration
├── pyproject.toml    # Project dependencies (uv)
└── README.md        # This file
```

## Database Schema

### Todo Model

| Field | Type | Description |
|-------|------|-------------|
| `todo_id` | Integer | Primary key (auto-increment) |
| `content` | String | Todo item description |
| `completed` | Boolean | Completion status (default: false) |


## Author

Created by [Suraj Yadav](https://github.com/suraj-yadav-aiml)
