from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import init_app
from .routers import auth, admin, user, chatbot

# Create FastAPI app
app = FastAPI(
    title="SpiritX Cricket Fantasy League API",
    description="API for cricket fantasy league management",
    version="1.0.0",
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database connection
init_app(app)

# Include routers
app.include_router(auth.router)
app.include_router(admin.router, prefix="/admin")
app.include_router(user.router, prefix="/user")
app.include_router(chatbot.router, prefix="/user")


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to SpiritX Cricket Fantasy League API",
        "version": "1.0.0",
        "documentation": "/docs",
    }


# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy"}
