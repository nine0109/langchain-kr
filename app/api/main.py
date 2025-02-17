from fastapi import FastAPI
from .api.endpoints import documents
from .core.logger import Logger

app = FastAPI()
logger = Logger("MainApp")

# 라우터 등록
app.include_router(documents.router, prefix="/documents", tags=["documents"])

@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy"}