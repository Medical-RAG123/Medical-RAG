from pathlib import Path

from app.api.ai.loaders.base import DocumentLoader
from app.api.ai.loaders.docx_loader import DocxLoader
from app.api.ai.loaders.markdown_loader import MarkdownLoader
from app.api.ai.loaders.pdf_loader import PDFLoader
from app.api.ai.loaders.text_loader import TextLoader


class DocumentLoaderFactory:
    @staticmethod
    def create(file_path: str) -> DocumentLoader:

        extension = Path(file_path).suffix.lower()

        if extension == ".pdf":
            return PDFLoader()

        elif extension == ".docx":
            return DocxLoader()

        elif extension == ".txt":
            return TextLoader()

        elif extension == ".md":
            return MarkdownLoader()

        else:
            raise ValueError(f"Unsupported file extension: {extension}")
