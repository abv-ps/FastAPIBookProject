# FastAPI Books & Authors Project

This is a minimal FastAPI project demonstrating:

- CRUD endpoints (GET, POST, PATCH, DELETE)
- Many-to-Many relationship (Books ↔ Authors)
- Background task example
- WebSocket support
- Docker and Docker Compose setup

---

## Initial project setup

1. **Create a `.env` file** in the root directory with the following keys:
    POSTGRES_DB=name_your_db
    POSTGRES_USER=your_user
    POSTGRES_PASSWORD=your_password
    POSTGRES_HOST=custom_postgres
    POSTGRES_PORT=5432

---

## To up the project

docker-compose up --build

2. Access services:

The application will be available at: http://localhost:8000

## API Endpoints
### Authors
POST /authors/ — create a new author

GET /authors/ — list all authors

### Books
POST /books/ — create a book and assign authors

GET /books/ — list all books with authors

PATCH /books/{id} — update book title or authors

DELETE /books/{id} — delete a book

### WebSocket
GET /ws — connect to WebSocket server
