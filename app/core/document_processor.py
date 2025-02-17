from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List, Dict
import os
from ..core.logger import Logger
from ..config import settings
import PyPDF2
from docx import Document
import pandas as pd

class DocumentProcessor:
    def __init__(self):
        self.logger = Logger("DocumentProcessor")
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.MAX_CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP,
            length_function=len,
        )
        
    def process_file(self, file_path: str) -> List[str]:
        """파일 형식에 따라 텍스트 추출"""
        try:
            extension = os.path.splitext(file_path)[1].lower()
            
            if extension == '.txt':
                return self._process_txt(file_path)
            elif extension == '.pdf':
                return self._process_pdf(file_path)
            elif extension == '.docx':
                return self._process_docx(file_path)
            elif extension in ['.csv', '.xlsx']:
                return self._process_tabular(file_path)
            else:
                raise ValueError(f"Unsupported file type: {extension}")
                
        except Exception as e:
            self.logger.error(f"Error processing file {file_path}: {str(e)}")
            raise
            
    def _process_txt(self, file_path: str) -> List[str]:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        return self.text_splitter.split_text(text)
        
    def _process_pdf(self, file_path: str) -> List[str]:
        texts = []
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                texts.extend(self.text_splitter.split_text(page.extract_text()))
        return texts
        
    def _process_docx(self, file_path: str) -> List[str]:
        doc = Document(file_path)
        text = ' '.join([paragraph.text for paragraph in doc.paragraphs])
        return self.text_splitter.split_text(text)
        
    def _process_tabular(self, file_path: str) -> List[str]:
        extension = os.path.splitext(file_path)[1].lower()
        if extension == '.csv':
            df = pd.read_csv(file_path)
        else:  # xlsx
            df = pd.read_excel(file_path)
            
        # 데이터프레임을 텍스트로 변환
        texts = []
        for _, row in df.iterrows():
            text = ' | '.join([f"{col}: {val}" for col, val in row.items()])
            texts.extend(self.text_splitter.split_text(text))
        return texts