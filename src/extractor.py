"""Extract text from research papers in multiple formats."""

import json
from typing import Dict, List, Optional, Tuple
from pathlib import Path
import PyPDF2
from docx import Document


class PaperExtractor:
    """Extracts text content from research papers."""

    @staticmethod
    def extract_from_pdf(pdf_path: str) -> str:
        """Extract text from PDF file."""
        text = []
        try:
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(pdf_reader.pages):
                    text.append(page.extract_text())
            return '\n'.join(text)
        except Exception as e:
            raise ValueError(f"Error extracting from PDF: {e}")

    @staticmethod
    def extract_from_docx(docx_path: str) -> str:
        """Extract text from Word document."""
        text = []
        try:
            doc = Document(docx_path)
            for para in doc.paragraphs:
                text.append(para.text)
            return '\n'.join(text)
        except Exception as e:
            raise ValueError(f"Error extracting from DOCX: {e}")

    @staticmethod
    def extract_from_txt(txt_path: str) -> str:
        """Extract text from plain text file."""
        try:
            with open(txt_path, 'r', encoding='utf-8') as file:
                return file.read()
        except Exception as e:
            raise ValueError(f"Error extracting from TXT: {e}")

    @staticmethod
    def extract_from_latex(latex_path: str) -> str:
        """Extract text from LaTeX file (basic extraction)."""
        try:
            with open(latex_path, 'r', encoding='utf-8') as file:
                content = file.read()
                # Basic LaTeX text extraction
                import re
                # Remove LaTeX commands but keep content
                text = re.sub(r'\\[a-zA-Z]+\{', '', content)
                text = re.sub(r'\}', '', text)
                text = re.sub(r'%.*$', '', text, flags=re.MULTILINE)
                return text
        except Exception as e:
            raise ValueError(f"Error extracting from LaTeX: {e}")

    @classmethod
    def extract_from_file(cls, file_path: str) -> str:
        """Auto-detect file type and extract text."""
        path = Path(file_path)
        suffix = path.suffix.lower()

        if suffix == '.pdf':
            return cls.extract_from_pdf(file_path)
        elif suffix == '.docx':
            return cls.extract_from_docx(file_path)
        elif suffix == '.txt':
            return cls.extract_from_txt(file_path)
        elif suffix in ['.tex', '.latex']:
            return cls.extract_from_latex(file_path)
        else:
            raise ValueError(f"Unsupported file format: {suffix}")

    @staticmethod
    def identify_sections(text: str) -> Dict[str, str]:
        """Identify major sections in the text."""
        sections = {}
        lines = text.split('\n')

        current_section = None
        current_content = []

        for line in lines:
            # Simple heuristic: lines that look like headers
            if line.strip() and (
                line.isupper() or 
                line.startswith(('Chapter', 'Section', 'Abstract', 'Introduction'))
            ):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line.strip()
                current_content = []
            elif current_section:
                current_content.append(line)

        if current_section:
            sections[current_section] = '\n'.join(current_content)

        return sections
