from fastapi import FastAPI

app = FastAPI(
    title="AI Invoice Intelligence",
    description="AI-powered financial document processing system",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "AI Invoice Intelligence API",
        "status": "running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "invoice-processing"
    }