import fitz  # PyMuPDF

class PDFExtractor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def extract_text_from_pdf(self):
        text = ""
        document = fitz.open(self.pdf_path)
        for page_num in range(len(document)):
            page = document.load_page(page_num)
            text += page.get_text()
        return text

    def chunk_text(self, text, max_tokens=9000):
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0

        for word in words:
            word_length = len(word) + 1  # Add 1 for the space
            if current_length + word_length > max_tokens:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_length = 0
            current_chunk.append(word)
            current_length += word_length

        if current_chunk:
            chunks.append(' '.join(current_chunk))

        return chunks
