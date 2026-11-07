from app.api.ai.loaders.base import DocumentLoader
from pypdf import PdfReader


class PDFLoader(DocumentLoader):
    def load(self, file_path: str) -> str:
        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:
            text = page.extract_text()

            if text and text.strip():
                pages.append(text.strip())

        return "\n\n".join(pages)
