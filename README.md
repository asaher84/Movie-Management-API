
# Movie Management API (FastAPI)

A clean, testable Backend assignment implementation using **FastAPI**, **SQLAlchemy**, and **SQLite** with full CRUD, pagination, unit tests, and auto-generated Swagger/OpenAPI docs.

## Tech Stack
- FastAPI (web framework, Swagger UI at `/docs`)
- Pydantic v2 (request/response validation)
- SQLAlchemy 2.x (ORM)
- SQLite (default DB; can switch via `DATABASE_URL`)
- Pytest (unit tests)
- python-dotenv (environment-based config, `.env` support)
- Uvicorn (ASGI server)
- Optional Dockerfile

## Project Structure
```
app/
  core/config.py           # Settings from env
  dao/db.py                # Engine/Session/Base
  dao/movie_repository.py  # DAO layer
  models/movie.py          # SQLAlchemy models
  schemas/movie.py         # Pydantic schemas + pagination
  services/movie_service.py# Business logic
  api/movies.py            # Handlers (routes)
  main.py                  # App entry
tests/
  test_movies.py
```

## Getting Started

### 1) Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) (Optional) Set environment variables
Create a `.env` file (see `.env.example`):
```
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=sqlite:///./movies.db
PAGE_LIMIT_DEFAULT=10
PAGE_LIMIT_MAX=50
```

### 4) Run the server
```bash
uvicorn app.main:app --reload
```
Open Swagger UI at: http://localhost:8000/docs

## API Endpoints

- `GET /movies?limit=&offset=` — List all movies with pagination
- `GET /movies/{id}` — Get movie by ID
- `POST /movies` — Create a new movie
- `PUT /movies/{id}` — Update existing movie
- `DELETE /movies/{id}` — Delete movie by ID

### Example request
```bash
curl -X POST http://localhost:8000/movies -H "Content-Type: application/json" -d '{
  "title": "Inception",
  "director": "Christopher Nolan",
  "releaseYear": 2010,
  "genre": "Sci-Fi",
  "rating": 9
}'
```

## Running Tests
```bash
pytest -q
```

## Docker
Build and run with Docker:
```bash
docker build -t movie-api .
docker run -p 8000:8000 --env-file .env movie-api
```

## Notes
- OpenAPI 3.0 spec is auto-generated; visit `/openapi.json`.
- Code is structured into **Handler → Service → DAO** layers for maintainability.
- Validation ensures `title` is required and `rating` is within 1–10.
