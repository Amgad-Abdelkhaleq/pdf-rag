from typing import List, Dict
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from src.core.config import settings

class DocumentService:
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """
        Extract text from a PDF file
        
        Args:
            file_path (str): Path to the PDF file
        
        Returns:
            str: Extracted text from the PDF
        """
        try:
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() or ""
            return text
        except Exception as e:
            raise ValueError(f"Error extracting text from PDF: {e}")
    
    @classmethod
    def chunk_document(cls, text: str) -> List[Dict[str, str]]:
        """
        Split document text into manageable chunks
        
        Args:
            text (str): Full document text
        
        Returns:
            List[Dict[str, str]]: List of document chunks
        """
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.CHUNK_SIZE,
            chunk_overlap=settings.CHUNK_OVERLAP
        )
        
        chunks = text_splitter.split_text(text)
        return [{"text": chunk} for chunk in chunks]