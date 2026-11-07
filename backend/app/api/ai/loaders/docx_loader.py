from app.api.ai.loaders.base import DocumentLoader
from docx import Document


class DocxLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        document = Document(file_path)

        paragraphs = []

        for paragraph in document.paragraphs:
            if paragraph.text.strip():
                paragraphs.append(paragraph.text.strip())

        return "\n".join(paragraphs)
