# LegalEase

LegalEase is an AI-powered legal-document template generator based on the supplied project specification. It uses:

- **Streamlit** for the frontend
- **FastAPI** for the backend API
- **Google Gemini** for document generation
- **python-docx** for DOCX export
- **FPDF2** for PDF export
- Plain UTF-8 TXT export
- Automated API/formatter tests with pytest

The supplied specification calls for Gemini 1.5 Pro and `google-generativeai`. Those are no longer the best current choices, so this implementation uses Google's current `google-genai` SDK and a configurable current Gemini model. The model can be changed with `GEMINI_MODEL`.

## Project structure

```text
LegalEase/
├── assets/
│   ├── logo.png
│   └── logo.svg
├── backend/
│   ├── ai_core/
│   │   ├── __init__.py
│   │   └── gemini_generator.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── document_formatter.py
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── models.py
│   └── routes.py
├── frontend/
│   └── app.py
├── tests/
│   ├── __init__.py
│   ├── test_api.py
│   └── test_formatters.py
├── .env.example
├── .gitignore
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 1. VS Code setup

1. Install Python 3.10+.
2. Open this `LegalEase` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

5. Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

6. Copy `.env.example` to `.env`.
7. Put your Gemini API key in `.env`:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-3.8-flash
```

Never commit `.env` to Git.

## 2. Run the backend

From the project root:

```bash
uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Open:

- API health: `http://127.0.0.1:8000/health`
- Swagger UI: `http://127.0.0.1:8000/docs`

A healthy response looks like:

```json
{"status":"ok","gemini_configured":true}
```

## 3. Run the Streamlit frontend

Open a second terminal, activate `.venv`, then:

```bash
streamlit run frontend/app.py
```

Open the address Streamlit prints, normally:

```text
http://localhost:8501
```

## 4. Test the application

Run automated tests:

```bash
pytest -q
```

The tests mock Gemini, so they do not spend API credits.

For an end-to-end manual test:

1. Start FastAPI.
2. Start Streamlit.
3. Enter a document type such as `Freelance Work Contract`.
4. Enter parties.
5. Enter semicolon-separated terms.
6. Enter an effective date.
7. Click **Generate Document**.
8. Review the generated preview.
9. Toggle **Edit Document** and modify the text.
10. Download TXT, DOCX, and PDF.

## 5. API example

```bash
curl -X POST "http://127.0.0.1:8000/api/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "document_type": "NDA",
    "parties": "Jane Doe (Discloser), TechNova Inc. (Recipient)",
    "terms": "Confidentiality for 2 years; Return confidential material on termination; No disclosure to third parties",
    "dates": "October 4, 2026"
  }'
```

## 6. Docker

Build and run:

```bash
docker compose up --build
```

Then open:

- Streamlit: `http://localhost:8501`
- FastAPI: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`

Set `GEMINI_API_KEY` in your shell or a local `.env` before starting Docker Compose.

## Design notes

### Validation
FastAPI/Pydantic validates all four required fields and applies sensible size limits.

### Security
The Gemini key stays on the backend. The Streamlit frontend only calls the FastAPI service.

### Prompt safety and factuality
The generator is instructed not to invent missing legal facts. Missing information is represented as a placeholder instead.

### Legal disclaimer
The app clearly presents generated material as an editable template rather than legal advice.

### Exports
DOCX includes Times New Roman formatting, a logo, a terms table, and a footer. PDF includes a branded header/footer. TXT is plain UTF-8.

### Extensibility
The AI generator, API routes, and document formatters are separated so another LLM provider or additional export format can be added without rewriting the UI.

## Production checklist

Before public deployment, add authentication, rate limiting, audit logging, encrypted persistence where needed, secrets management, stricter CORS, structured logging, monitoring, and a privacy/data-retention policy appropriate for sensitive legal documents.
