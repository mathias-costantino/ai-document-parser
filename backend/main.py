from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import upload

app = FastAPI(title="AI Document Parser")

# CORS (per permettere al frontend di chiamare le API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints base
@app.get("/")
def read_root():
    return {"message": "AI Document Parser API", "version": "1.0"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Include router upload
app.include_router(upload.router, prefix="/api", tags=["upload"])