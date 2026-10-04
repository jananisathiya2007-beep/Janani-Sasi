from fastapi import APIRouter, HTTPException
from backend.models import DocumentRequest, DocumentResponse
from backend.ai_core.gemini_generator import GeminiDocumentGenerator

router = APIRouter(prefix="/api", tags=["documents"])

@router.post("/generate", response_model=DocumentResponse)
def generate_document(request: DocumentRequest):
    try:
        generator = GeminiDocumentGenerator()
        content = generator.generate_document(request)
        return DocumentResponse(document_type=request.document_type, content=content)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"AI generation failed: {exc}") from exc
