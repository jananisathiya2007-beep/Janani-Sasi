import os
from pathlib import Path
import html

import requests
import streamlit as st
from dotenv import load_dotenv

from backend.services.document_formatter import format_docx, format_pdf, format_txt, format_html_preview

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")
LOGO = Path(__file__).resolve().parents[1] / "assets" / "logo.png"

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

st.markdown("""
<style>
.block-container {max-width: 1150px; padding-top: 2rem;}
.hero {padding: 1.2rem 1.4rem; border: 1px solid #334155; border-radius: 16px;
       background: linear-gradient(135deg,#0f172a,#1e293b); color: white; margin-bottom: 1rem;}
.preview {padding: 24px; border-radius: 14px; background:#0b1220; color:#e5e7eb;
          border:1px solid #334155; max-height:620px; overflow:auto; line-height:1.7;}
.small-note {color:#64748b; font-size:.9rem;}
</style>
""", unsafe_allow_html=True)

if LOGO.exists():
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.image(str(LOGO), width=110)

st.markdown(
    '<div class="hero"><h1>LegalEase</h1>'
    '<p>AI-powered legal document templates with editable previews and TXT, DOCX, and PDF export.</p></div>',
    unsafe_allow_html=True,
)

with st.form("document_form"):
    left, right = st.columns(2)
    with left:
        document_type = st.text_input("Document Type", placeholder="Freelance Work Contract")
        parties = st.text_area(
            "Parties Involved",
            placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
            height=120,
        )
    with right:
        dates = st.text_input("Effective Date", placeholder="April 10, 2026")
        terms = st.text_area(
            "Terms & Conditions",
            placeholder="Payment within 30 days; Confidentiality maintained; Either party may terminate with 15 days notice",
            height=120,
        )
    submitted = st.form_submit_button("Generate Document", type="primary", use_container_width=True)

if submitted:
    if not all([document_type.strip(), parties.strip(), dates.strip(), terms.strip()]):
        st.error("Please complete all fields.")
    else:
        with st.spinner("Generating your document..."):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/generate",
                    json={
                        "document_type": document_type,
                        "parties": parties,
                        "terms": terms,
                        "dates": dates,
                    },
                    timeout=120,
                )
                if response.ok:
                    data = response.json()
                    st.session_state["document"] = data["content"]
                    st.session_state["document_type"] = data["document_type"]
                    st.success("Document generated.")
                else:
                    try:
                        detail = response.json().get("detail", response.text)
                    except Exception:
                        detail = response.text
                    st.error(f"Backend error ({response.status_code}): {detail}")
            except requests.RequestException as exc:
                st.error(f"Could not reach FastAPI at {BACKEND_URL}. Start the backend first. Details: {exc}")

if "document" in st.session_state:
    st.divider()
    st.subheader("Document Preview")

    edit = st.toggle("Edit Document", value=False)
    if edit:
        st.session_state["document"] = st.text_area(
            "Editable document",
            value=st.session_state["document"],
            height=600,
        )
    else:
        preview = format_html_preview(st.session_state["document"])
        st.markdown(f'<div class="preview">{preview}</div>', unsafe_allow_html=True)

    content = st.session_state["document"]
    doc_type = st.session_state["document_type"]
    slug = "".join(c.lower() if c.isalnum() else "_" for c in doc_type).strip("_") or "document"

    st.subheader("Download")
    b1, b2, b3 = st.columns(3)
    with b1:
        st.download_button("Download TXT", format_txt(content), f"{slug}.txt", "text/plain", use_container_width=True)
    with b2:
        st.download_button("Download DOCX", format_docx(content, doc_type, terms), f"{slug}.docx",
                           "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                           use_container_width=True)
    with b3:
        st.download_button("Download PDF", format_pdf(content, doc_type), f"{slug}.pdf",
                           "application/pdf", use_container_width=True)

st.caption("LegalEase generates templates, not legal advice. Review documents with a qualified legal professional before relying on them.")
