# FastAPI Book Collection MCP Server

A Model Context Protocol (MCP) server built with FastAPI for managing a book collection. This application provides both a RESTful API and MCP tool integration for performing CRUD operations on books stored in a SQLite database.

## Features

- Complete CRUD operations for book management
- FastAPI with automatic OpenAPI documentation
- SQLite database with SQLAlchemy ORM
- Model Context Protocol (MCP) integration
- Pydantic models for data validation
- Interactive API documentation
- Pagination support for book listings
- Automatic database initialization

## Prerequisites

- Python 3.13 or higher
- No external dependencies (uses SQLite)

## Installation

1. Clone or download this project
2. Install dependencies using uv:
   ```bash
   uv sync
   ```

   Or using pip:
   ```bash
   pip install fastapi[standard] sqlalchemy pydantic uvicorn fastapi-mcp
   ```

## Usage

### Running the Server

Start the FastAPI server with MCP integration:

```bash
python main.py
```

This will start the server on `http://127.0.0.1:8000` with both REST API and MCP capabilities.

Alternatively, you can run with uvicorn directly:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

### Accessing the API

- **Interactive Documentation**: `http://127.0.0.1:8000/docs` (Swagger UI)
- **Alternative Documentation**: `http://127.0.0.1:8000/redoc` (ReDoc)
- **Root Endpoint**: `http://127.0.0.1:8000/` (Welcome page with links)

## API Endpoints

### Root
- **GET /**: Welcome message with navigation links
  - Returns: Welcome message and links to documentation and book list

### Books Management

- **GET /books**: Retrieve all books with pagination
  - Query Parameters:
    - `skip` (int, default=0): Number of books to skip
    - `limit` (int, default=10): Maximum number of books to return
  - Returns: List of books

- **GET /books/{book_id}**: Retrieve a specific book
  - Path Parameters:
    - `book_id` (int): Unique identifier of the book
  - Returns: Book details or 404 if not found

- **POST /books**: Create a new book
  - Request Body:
    ```json
    {
      "title": "Book Title",
      "read": false
    }
    ```
  - Returns: Created book with assigned ID

- **PUT /books/{book_id}**: Update an existing book
  - Path Parameters:
    - `book_id` (int): Unique identifier of the book
  - Request Body:
    ```json
    {
      "title": "Updated Book Title",
      "read": true
    }
    ```
  - Returns: Updated book details or 404 if not found

- **DELETE /books/{book_id}**: Delete a book
  - Path Parameters:
    - `book_id` (int): Unique identifier of the book
  - Returns: Deleted book details or 404 if not found

## Data Models

### Book Model (Database)
```python
class Book(Base):
    id: int (Primary Key)
    title: str (Indexed)
    read: bool (Default: False)
```

### Request/Response Models

**BookCreate (Request)**
```python
{
  "title": "string",
  "read": false  # Optional, defaults to false
}
```

**BookResponse (Response)**
```python
{
  "id": 1,
  "title": "string",
  "read": false
}
```

## MCP Integration

This server includes Model Context Protocol (MCP) integration using FastAPI-MCP, which exposes the following operations as MCP tools:

- `get_books` - Retrieve all books
- `get_book` - Retrieve a specific book by ID
- `create_book` - Create a new book
- `update_book` - Update an existing book
- `delete_book` - Delete a book

These tools can be used by MCP-compatible clients and AI assistants for book management operations.

### MCP Tool Usage Example

```python
# The MCP tools are automatically exposed and can be called by MCP clients
# Example operations available:
# - get_books(skip=0, limit=10)
# - get_book(book_id=1)
# - create_book(title="New Book", read=False)
# - update_book(book_id=1, title="Updated Title", read=True)
# - delete_book(book_id=1)
```

## Database

The application uses SQLite for data storage with the following characteristics:

- **Database File**: `test.db` (automatically created)
- **ORM**: SQLAlchemy with declarative base
- **Connection**: SQLite with automatic session management
- **Initialization**: Tables are created automatically on startup

### Database Schema

```sql
CREATE TABLE books (
    id INTEGER PRIMARY KEY,
    title VARCHAR,
    read BOOLEAN
);
```

## Example Usage

### Using cURL

**Create a book:**
```bash
curl -X POST "http://127.0.0.1:8000/books" \
     -H "Content-Type: application/json" \
     -d '{"title": "The Great Gatsby", "read": false}'
```

**Get all books:**
```bash
curl -X GET "http://127.0.0.1:8000/books"
```

**Update a book:**
```bash
curl -X PUT "http://127.0.0.1:8000/books/1" \
     -H "Content-Type: application/json" \
     -d '{"title": "The Great Gatsby", "read": true}'
```

### Using Python Requests

```python
import requests

# Create a book
response = requests.post(
    "http://127.0.0.1:8000/books",
    json={"title": "1984", "read": False}
)
book = response.json()
print(f"Created book: {book}")

# Get all books
response = requests.get("http://127.0.0.1:8000/books")
books = response.json()
print(f"All books: {books}")

# Mark book as read
book_id = book["id"]
response = requests.put(
    f"http://127.0.0.1:8000/books/{book_id}",
    json={"title": "1984", "read": True}
)
updated_book = response.json()
print(f"Updated book: {updated_book}")
```

## Development

### Project Structure

```
mcp-fastapi-server/
├── main.py              # Main FastAPI application
├── pyproject.toml       # Project configuration
├── README.md           # This file
├── test.db             # SQLite database (created at runtime)
├── uv.lock             # Dependency lock file
└── .gitignore          # Git ignore rules
```

### Dependencies

- **FastAPI**: Modern, fast web framework for APIs
- **SQLAlchemy**: SQL toolkit and ORM
- **Pydantic**: Data validation using Python type hints
- **Uvicorn**: Lightning-fast ASGI server
- **FastAPI-MCP**: Model Context Protocol integration for FastAPI

### Running in Development Mode

For development with auto-reload:
```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

## Error Handling

The API includes proper error handling:

- **404 Not Found**: When a book with the specified ID doesn't exist
- **422 Unprocessable Entity**: When request data validation fails
- **500 Internal Server Error**: For unexpected server errors

Error responses follow the FastAPI standard format:
```json
{
  "detail": "Book not found"
}
```

## Testing

You can test the API using:

1. **Interactive Documentation**: Visit `/docs` for Swagger UI testing
2. **cURL**: Use command-line HTTP requests
3. **Python Requests**: Programmatic API testing
4. **Postman**: Import the OpenAPI specification from `/openapi.json`

## Configuration

The application uses the following default configuration:

- **Host**: 127.0.0.1 (localhost)
- **Port**: 8000
- **Database**: SQLite (`test.db`)
- **Auto-reload**: Disabled in production

To modify configuration, edit the `uvicorn.run()` call in `main.py`.

## Troubleshooting

### Common Issues

1. **Port already in use**
   - Change the port in `main.py` or kill the process using port 8000

2. **Database permission errors**
   - Ensure write permissions in the application directory

3. **Import errors**
   - Verify all dependencies are installed: `uv sync`

4. **MCP tools not working**
   - Ensure FastAPI-MCP is properly installed and configured

### Logging

The application uses FastAPI's built-in logging. For more detailed logs, run with:
```bash
uvicorn main:app --log-level debug
```

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is provided as-is for educational and development purposes.
