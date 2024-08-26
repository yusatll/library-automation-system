import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from fastapi import FastAPI
from .routers import books, patrons, operations
from .dependencies import create_tables

app = FastAPI(title="Library Automation System")

# Create tables
logger.info("Creating database tables...")
create_tables()
logger.info("Database tables created.")

app.include_router(books.router, prefix="/api", tags=["books"])
app.include_router(patrons.router, prefix="/api", tags=["patrons"])
app.include_router(operations.router, prefix="/api", tags=["operations"])

@app.get("/")
async def root():
    logger.info("Root endpoint called.")
    return {"message": "Welcome to the Library Automation System"}