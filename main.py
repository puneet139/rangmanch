from contextlib import asynccontextmanager
from fastapi import FastAPI
from database import create_tables
from routes.reviews import router as reviews_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Perform any startup tasks here
    create_tables()
    print("Database tables created successfully.")
    yield
    print("Application is shutting down.")
    # Perform any cleanup tasks here

app = FastAPI(
    title="Rangmanch review API",
    description="API for managing play reviews",
    version="0.0.1",
    lifespan=lifespan)

app.include_router(reviews_router)
@app.get("/")
def root():
    return {"message": "Welcome to the Rangmanch review API!"}