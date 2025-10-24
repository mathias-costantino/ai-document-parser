from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World - AI Document Parser"}

@app.get("/health")
def health_check():
    return {"status": "ok"}