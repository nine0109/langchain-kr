from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # 기본 설정
    PROJECT_NAME: str = "RAG System"
    API_V1_STR: str = "/api/v1"
    
    # 파일 관련 설정
    UPLOAD_DIR: str = "uploads"
    VECTORDB_DIR: str = "vectordb"
    MAX_CHUNK_SIZE: int = 1000
    CHUNK_OVERLAP: int = 200
    
    # 임베딩 모델 설정
    EMBEDDING_MODEL: str = "jhgan/ko-sbert-nli"
    DEVICE: str = "cuda"
    
    # LLM 설정
    OPENWEBUI_BASE_URL: str = "http://localhost:8080"
    DEFAULT_MODEL: str = "deepseek"
    
    # 벡터 DB 설정
    VECTORDB_SAVE_INTERVAL: int = 10  # 10개 문서마다 저장
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()