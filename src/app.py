"""
Main FastAPI application entry point for the F1 Stats Explorer project.

This module:
- Initializes the FastAPI app
- Configures CORS middleware
- Registers API routes
- Serves static files
- Renders the main HTML frontend using Jinja2 templates
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from src.api import routes

# Initialize FastAPI application
app = FastAPI(
    title="F1 Stats Explorer API",
    description="API for retrieving and visualizing Formula 1 statistics using Jolpica data.",
    version="1.0.0"
)

# Configure CORS middleware
# In production, restrict allow_origins to specific domains.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Include API routes from src/api/routes.py
app.include_router(routes.router)

# Configure Jinja2 template directory
templates = Jinja2Templates(directory="src/templates")

# Serve static files (CSS, JS, images, favicon)
app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Render the main frontend page.

    This endpoint serves the primary HTML interface
    for the F1 Stats Explorer dashboard.

    Args:
        request (Request): FastAPI request object (required by Jinja2).

    Returns:
        HTMLResponse: Rendered index.html template.
    """
    return templates.TemplateResponse("index.html", {"request": request})