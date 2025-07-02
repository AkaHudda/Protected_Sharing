from fastapi import FastAPI
from app.user_routes import router as user_router
from app.file_routes import router as file_router

app = FastAPI(
    title="Secure File Sharing System",
    description="File upload/download system for Ops and Client users",
    version="1.0.0"
)

# Include all routers
app.include_router(user_router, prefix="/client", tags=["Client"])
app.include_router(file_router, tags=["File Operations"])
