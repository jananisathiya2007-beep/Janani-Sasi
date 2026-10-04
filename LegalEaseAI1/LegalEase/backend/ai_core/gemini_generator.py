from backend.config import get_settings
from backend.models import DocumentRequest

SYSTEM_INSTRUCTION = """
You are LegalEase, an AI assistant that drafts structured legal-document templates.
You are not a lawyer and must not claim that generated text is legally valid, jurisdiction-specific,
or a substitute for legal advice.

Produce a professional editable draft from the user's supplied facts. Never invent names, dates,
addresses, amounts, laws, court citations, or obligations that were not supplied. If a necessary
fact is missing, use a clear bracketed placeholder such as [MISSING INFORMATION] rather than guessing.

Use plain text/Markdown-compatible formatting:
TITLE
PARTIES
EFFECTIVE DATE
1. PURPOSE
2. TERMS AND CONDITIONS
3. CONFIDENTIALITY (when relevant)
4. TERMINATION (when relevant)
5. GOVERNING LAW (only if the user supplied it)
6. SIGNATURES

Adapt the sections to the requested document type. Preserve the user's terms faithfully.
End with:
IMPORTANT: This is an AI-generated template for review and editing. Obtain qualified legal advice
before relying on it.
"""

class GeminiDocumentGenerator:
    def __init__(self, api_key: str | None = None, model: str | None = None):
        settings = get_settings()
        self.api_key = api_key or settings.gemini_api_key
        self.model = model or settings.gemini_model
        self._client = None
        if self.api_key:
            try:
                from google import genai
                self._client = genai.Client(api_key=self.api_key)
            except ImportError as exc:
                raise RuntimeError(
                    "The Gemini SDK is not installed. Run: pip install -r requirements.txt"
                ) from exc

    @property
    def configured(self) -> bool:
        return self._client is not None

    def generate_document(self, request: DocumentRequest) -> str:
        if not self._client:
            raise RuntimeError("GEMINI_API_KEY is not configured. Add it to your .env file.")

        prompt = f"""
Create a complete draft of a {request.document_type}.

PARTIES:
{request.parties}

EFFECTIVE DATE / DATE DETAILS:
{request.dates}

USER-PROVIDED TERMS:
{request.terms}

Return only the draft document. Do not add a preamble about being an AI.
"""
        from google.genai import types
        response = self._client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
                max_output_tokens=6000,
            ),
        )
        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text
