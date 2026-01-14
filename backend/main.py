from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.task_routes import router as task_router
from src.api.auth_routes import router as auth_router
from src.db.database import create_db_and_tables
import uvicorn

app = FastAPI(title="Todo App API", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_origin_regex=r"https?://localhost(:[0-9]+)?|https?://127\.0\.0\.1(:[0-9]+)?",
)

# Include routers
app.include_router(task_router, prefix="/api", tags=["tasks"])
app.include_router(auth_router, prefix="/api", tags=["auth"])

@app.on_event("startup")
async def startup_event():
    await create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo App API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
