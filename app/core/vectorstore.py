# from langchain_community.vectorstores import FAISS
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from typing import List
# from .logger import Logger

# class VectorStore:
#     def __init__(self):
#         self.logger = Logger("VectorStore")
#         self.embeddings = HuggingFaceEmbeddings(
#             model_name="jhgan/ko-sbert-nli",
#             model_kwargs={'device': 'cuda'}
#         )
#         self.vectorstore = None
        
#     async def create_or_update(self, texts: List[str], force_rebuild: bool = False):
#         try:
#             if force_rebuild or not self.vectorstore:
#                 self.logger.info("Creating new vector store")
#                 self.vectorstore = FAISS.from_texts(texts, self.embeddings)
#             else:
#                 self.logger.info("Updating existing vector store")
#                 self.vectorstore.add_texts(texts)
#             return True
#         except Exception as e:
#             self.logger.error(f"Error in vector store operation: {str(e)}")
#             raise



from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from typing import List, Optional
from .logger import Logger
from ..config import settings
import os
import shutil
import time

class VectorStore:
    def __init__(self):
        self.logger = Logger("VectorStore")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.EMBEDDING_MODEL,
            model_kwargs={'device': settings.DEVICE}
        )
        self.vectorstore = None
        self.last_save_time = time.time()
        self.docs_since_save = 0
        
        # 벡터 DB 디렉토리 생성
        if not os.path.exists(settings.VECTORDB_DIR):
            os.makedirs(settings.VECTORDB_DIR)
            
        # 기존 벡터 DB 로드 시도
        self._load_vectorstore()
        
    def _load_vectorstore(self):
        """저장된 벡터 DB 로드"""
        try:
            if os.path.exists(os.path.join(settings.VECTORDB_DIR, "index.faiss")):
                self.logger.info("Loading existing vector store")
                self.vectorstore = FAISS.load_local(
                    settings.VECTORDB_DIR,
                    self.embeddings
                )
        except Exception as e:
            self.logger.error(f"Error loading vector store: {str(e)}")
            self.vectorstore = None
            
    def _save_vectorstore(self):
        """벡터 DB 저장"""
        if self.vectorstore:
            try:
                # 임시 디렉토리에 저장 후 이동 (atomic operation)
                temp_dir = f"{settings.VECTORDB_DIR}_temp"
                self.vectorstore.save_local(temp_dir)
                
                # 기존 디렉토리 삭제 후 임시 디렉토리 이동
                if os.path.exists(settings.VECTORDB_DIR):
                    shutil.rmtree(settings.VECTORDB_DIR)
                shutil.move(temp_dir, settings.VECTORDB_DIR)
                
                self.last_save_time = time.time()
                self.docs_since_save = 0
                self.logger.info("Vector store saved successfully")
                
            except Exception as e:
                self.logger.error(f"Error saving vector store: {str(e)}")
                raise
                
    async def add_texts(self, texts: List[str]):
        """텍스트 추가"""
        try:
            if not self.vectorstore:
                self.vectorstore = FAISS.from_texts(texts, self.embeddings)
            else:
                self.vectorstore.add_texts(texts)
                
            self.docs_since_save += len(texts)
            
            # 저장 간격 확인
            if self.docs_since_save >= settings.VECTORDB_SAVE_INTERVAL:
                self._save_vectorstore()
                
            return True
            
        except Exception as e:
            self.logger.error(f"Error adding texts: {str(e)}")
            raise
            
    async def create_or_update(self, texts: List[str], force_rebuild: bool = False):
        """벡터 DB 생성 또는 업데이트"""
        try:
            if force_rebuild:
                self.logger.info("Forcing vector store rebuild")
                self.vectorstore = FAISS.from_texts(texts, self.embeddings)
            else:
                await self.add_texts(texts)
                
            self._save_vectorstore()
            return True
            
        except Exception as e:
            self.logger.error(f"Error in vector store operation: {str(e)}")
            raise