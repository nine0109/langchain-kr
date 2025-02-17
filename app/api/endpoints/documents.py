from fastapi import APIRouter, UploadFile, File
from ...core.logger import Logger
from ...models.schemas import DocumentUpload, VectorDBUpdate
from ...core.vectorstore import VectorStore
import os
from typing import List

router = APIRouter()
logger = Logger("DocumentsAPI")
vector_store = VectorStore()

@router.post("/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    try:
        logger.info(f"Receiving {len(files)} documents for upload")
        
        # 임시 저장 디렉토리
        upload_dir = "uploads"
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)
            
        saved_files = []
        for file in files:
            file_path = os.path.join(upload_dir, file.filename)
            with open(file_path, "wb") as buffer:
                content = await file.read()
                buffer.write(content)
            saved_files.append(file_path)
            
        logger.info(f"Successfully saved {len(saved_files)} files")
        return {"message": "Files uploaded successfully", "files": saved_files}
        
    except Exception as e:
        logger.error(f"Error in document upload: {str(e)}")
        raise

@router.post("/vectordb/update")
async def update_vectordb(update_request: VectorDBUpdate):
    try:
        logger.info("Starting vector database update")
        
        # 여기서 저장된 문서들을 처리하고 벡터 DB 업데이트
        # 실제 구현에서는 문서 처리 로직 추가 필요
        
        await vector_store.create_or_update(
            texts=["Sample text"],  # 실제 문서 텍스트로 교체 필요
            force_rebuild=update_request.force_rebuild
        )
        
        logger.info("Vector database update completed")
        return {"message": "Vector database updated successfully"}
        
    except Exception as e:
        logger.error(f"Error in vector database update: {str(e)}")
        raise