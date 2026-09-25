# MCP Demo

A small [FastMCP](https://gofastmcp.com/) server that exposes todo tools over MCP. Todos are stored in a local JSON file next to the server module.

## Requirements

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Setup

```bash
git clone <repo-url>
cd MCP-Demo
uv sync
```

## Run the server

stdio (what Cursor uses):

```bash
uv run python src/mcp_demo/MCPServer.py
```

The server process talks MCP on stdin/stdout. You do not need to activate a virtualenv by hand if you use `uv run`.

## Connect from Cursor

Project config lives in `.cursor/mcp.json`. Point `cwd` at this repo and `command` at your `uv` binary:

```json
{
  "mcpServers": {
    "todo": {
      "command": "uv",
      "args": ["run", "python", "src/mcp_demo/MCPServer.py"],
      "cwd": "/absolute/path/to/MCP-Demo"
    }
  }
}
```

Reload the **todo** MCP server in Cursor after you change `MCPServer.py`.

## Tools

| Tool | Purpose |
|------|---------|
| `create_todo` | Create a todo (`title` required; optional `description`, `Status`) |
| `list_todo` | List todos, optionally filtered by status |
| `get_todo` | Fetch one todo by id |
| `delete_todo` | Delete a todo by id |

Status values: `Pending`, `Complete`, `Deleted`.

Each todo has `id` (8-character hex), `title`, `description` (truncated to 100 characters), `status`, `created_at`, and `updated_at` (UTC ISO timestamps).

## Data

Todos are persisted in `src/mcp_demo/todos.json`. The file is created on first successful save.

## Project layout

```
src/mcp_demo/MCPServer.py   # FastMCP todo server
.cursor/mcp.json            # Cursor MCP launch config
pyproject.toml              # package metadata and dependencies
```
