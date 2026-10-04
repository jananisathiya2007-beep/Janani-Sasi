from fastapi.testclient import TestClient
import backend.routes as routes
from backend.main import app

client = TestClient(app)

class FakeGenerator:
    def __init__(self, *args, **kwargs):
        pass
    def generate_document(self, request):
        return "# TEST AGREEMENT\n\nThis is a generated test document."

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "LegalEase API"

def test_generate(monkeypatch):
    monkeypatch.setattr(routes, "GeminiDocumentGenerator", FakeGenerator)
    response = client.post("/api/generate", json={
        "document_type": "NDA",
        "parties": "A (Discloser), B (Recipient)",
        "terms": "Keep information confidential; Return materials on termination",
        "dates": "October 4, 2026",
    })
    assert response.status_code == 200
    assert "TEST AGREEMENT" in response.json()["content"]

def test_validation():
    response = client.post("/api/generate", json={
        "document_type": "",
        "parties": "A",
        "terms": "B",
        "dates": "C",
    })
    assert response.status_code == 422
