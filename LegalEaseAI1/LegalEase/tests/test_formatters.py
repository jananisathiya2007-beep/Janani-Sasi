from docx import Document
from backend.services.document_formatter import format_docx, format_pdf, format_txt, sanitize_text

def test_sanitize_text():
    assert sanitize_text("Hello\u2014world\u00a0!") == "Hello-world !"

def test_txt():
    assert format_txt("Hello") == b"Hello"

def test_docx():
    data = format_docx("# NDA\n\nConfidential.", "NDA", "Keep secret; Return materials")
    assert data[:2] == b"PK"
    doc = Document(__import__("io").BytesIO(data))
    assert any("NDA" in p.text for p in doc.paragraphs)

def test_pdf():
    data = format_pdf("NDA\n\nConfidential.", "NDA")
    assert data.startswith(b"%PDF")
