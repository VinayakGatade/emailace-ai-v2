from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from database import create_tables
from routes import router
from seed_data import seed_database

# Global variable to track if database is initialized
db_initialized = False

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    global db_initialized
    
    # Startup
    print("🚀 Starting EmailAce AI Backend...")
    
    # Create database tables
    create_tables()
    print("✅ Database tables created")
    
    # Seed database with sample data
    if not db_initialized:
        seed_database()
        db_initialized = True
        print("✅ Database seeded with sample emails")
    
    print("🎯 Backend ready! Visit http://127.0.0.1:8000/docs for API docs")
    
    yield
    
    # Shutdown
    print("👋 Shutting down EmailAce AI Backend...")

# Create FastAPI app
app = FastAPI(
    title="EmailAce AI - Email Communication Assistant",
    description="AI-powered email management system with sentiment analysis, urgency detection, and automated reply generation",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware with comprehensive configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000", 
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["emails"])

# Global OPTIONS handler for all routes
@app.options("/{path:path}")
async def options_handler(request: Request, path: str):
    """Handle preflight OPTIONS requests for all routes"""
    return JSONResponse(
        content={"message": "OK"},
        headers={
            "Access-Control-Allow-Origin": request.headers.get("origin", "*"),
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "Accept, Accept-Language, Content-Language, Content-Type, Authorization, X-Requested-With, Origin, Access-Control-Request-Method, Access-Control-Request-Headers",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Max-Age": "86400",
        }
    )

# Root endpoint redirect
@app.get("/")
async def root():
    """Redirect to health check"""
    return {"message": "Welcome to EmailAce AI! Use /api/v1/ for API endpoints"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )


