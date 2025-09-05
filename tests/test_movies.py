
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.dao.db import Base
from app.main import app
from app.api.movies import get_db

# Use an in-memory SQLite database for tests
SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, future=True)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def test_create_movie():
    payload = {"title": "Inception", "director": "Christopher Nolan", "releaseYear": 2010, "genre": "Sci-Fi", "rating": 9}
    r = client.post("/movies", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Inception"
    assert "id" in data

def test_list_movies_pagination():
    # Ensure at least 2 movies exist
    for i in range(2):
        client.post("/movies", json={"title": f"Movie {i}", "rating": 7})
    r = client.get("/movies?limit=2&offset=0")
    assert r.status_code == 200
    data = r.json()
    assert "items" in data and "total" in data and "limit" in data and "offset" in data
    assert data["limit"] == 2
    assert len(data["items"]) <= 2

def test_get_update_delete_movie():
    # create
    r = client.post("/movies", json={"title": "Interstellar", "rating": 8.5})
    movie_id = r.json()["id"]

    # get
    r = client.get(f"/movies/{movie_id}")
    assert r.status_code == 200
    assert r.json()["title"] == "Interstellar"

    # update
    r = client.put(f"/movies/{movie_id}", json={"rating": 9.5})
    assert r.status_code == 200
    assert r.json()["rating"] == 9.5

    # delete
    r = client.delete(f"/movies/{movie_id}")
    assert r.status_code == 204

    # get should 404
    r = client.get(f"/movies/{movie_id}")
    assert r.status_code == 404
