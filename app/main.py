
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from app.api.movies import router as movies_router
from app.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="A basic Movie Management API with CRUD, pagination, and Swagger docs."
)

app.include_router(movies_router)

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")
