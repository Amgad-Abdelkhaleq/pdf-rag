from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from src.api.routes import document, chat
from src.core.config import settings

def create_app():
    """
    Create and configure FastAPI application
    
    Returns:
        FastAPI: Configured application instance
    """
    app = FastAPI(title=settings.PROJECT_NAME)
    
    # CORS Middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routes
    app.include_router(document.router, prefix="/documents", tags=["documents"])
    app.include_router(chat.router, tags=["chat"])
    
    return app

def run_api():
    """
    Run FastAPI application
    """
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    run_api()