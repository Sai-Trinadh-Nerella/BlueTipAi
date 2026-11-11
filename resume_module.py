import hashlib
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from io import BytesIO

import streamlit as st

MAX_RESUME_SIZE = 5 * 1024 * 1024

SKILL_KEYWORDS = [
    "Python", "Java", "JavaScript", "TypeScript", "C", "C++", "C#", "SQL", "HTML", "CSS",
    "React", "Angular", "Vue", "Streamlit", "FastAPI", "Flask", "Django", "Spring Boot",
    "Node.js", "Express", "Pandas", "NumPy", "scikit-learn", "TensorFlow", "PyTorch",
    "Machine Learning", "Deep Learning", "NLP", "Generative AI", "RAG", "LangChain",
    "PostgreSQL", "MySQL", "MongoDB", "ChromaDB", "Redis", "AWS", "Azure", "GCP",
    "Docker", "Kubernetes", "Git", "GitHub", "Power BI", "Tableau", "Excel"
]
EDUCATION_TERMS = ["b.tech", "b.e.", "bachelor", "b.sc", "bca", "m.tech", "m.e.", "master", "m.sc", "mca", "ph.d", "phd", "diploma", "intermediate", "high school", "ssc", "hsc"]
CERTIFICATION_TERMS = ["certification", "certified", "certificate", "certifications"]


def extract_document_text(uploaded_file):
    extension = uploaded_file.name.rsplit(".", 1)[-1].lower()
    file_bytes = uploaded_file.getvalue()

    if extension == "pdf":
        from pypdf import PdfReader
        reader = PdfReader(BytesIO(file_bytes))
        return "\n".join(page.extract_text() or "" for page in reader.pages)

    if extension == "docx":
        from docx import Document
        document = Document(BytesIO(file_bytes))
        parts = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        for table in document.tables:
            for row in table.rows:
                parts.append(" | ".join(cell.text.strip() for cell in row.cells if cell.text.strip()))
        return "\n".join(parts)

    if extension == "doc":
        antiword = shutil.which("antiword")
        if antiword:
            result = subprocess.run([antiword, "-"], input=file_bytes, capture_output=True, check=True)
            return result.stdout.decode("utf-8", errors="ignore")
        try:
            import win32com.client
            with tempfile.TemporaryDirectory() as temp_dir:
                source_path = Path(temp_dir) / uploaded_file.name
                text_path = Path(temp_dir) / "resume.txt"
                source_path.write_bytes(file_bytes)
                word = win32com.client.DispatchEx("Word.Application")
                word.Visible = False
                document = word.Documents.Open(str(source_path.resolve()), ReadOnly=True)
                document.SaveAs2(str(text_path.resolve()), FileFormat=2)
                document.Close(False)
                word.Quit()
                return text_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as exc:
            raise RuntimeError("This .doc file was received, but text extraction requires Microsoft Word with pywin32 or the Antiword utility. Converting it to .docx or PDF is the easiest workaround.") from exc

    raise ValueError("Unsupported file type. Upload PDF, DOC or DOCX.")


def extract_candidate_fields(text):
    clean_lines = [re.sub(r"\s+", " ", line).strip(" |\t") for line in text.splitlines()]
    lines = [line for line in clean_lines if line]
    joined = "\n".join(lines)

    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", joined)
    phone_match = re.search(r"(?:\+?91[\s-]?)?[6-9]\d{9}\b|\b\d{3}[\s.-]\d{3}[\s.-]\d{4}\b", joined)

    full_name = ""
    for line in lines[:12]:
        if len(line) <= 70 and not re.search(r"@|https?://|resume|curriculum vitae|\d{5,}", line, re.I):
            words = line.split()
            if 2 <= len(words) <= 5 and all(re.fullmatch(r"[A-Za-z][A-Za-z.'-]*", word) for word in words):
                full_name = line
                break

    skills_found = []
    lower_text = joined.lower()
    for skill in SKILL_KEYWORDS:
        if re.search(r"(?<![a-z0-9+#])" + re.escape(skill.lower()) + r"(?![a-z0-9+#])", lower_text):
            skills_found.append(skill)

    education_lines = [line for line in lines if any(term in line.lower() for term in EDUCATION_TERMS)]
    certification_lines = [line for line in lines if any(term in line.lower() for term in CERTIFICATION_TERMS)]

    experience_match = re.search(r"(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)\s+(?:of\s+)?experience", joined, re.I)
    if not experience_match:
        experience_match = re.search(r"experience\s*[:\-]?\s*(\d+(?:\.\d+)?)\s*\+?\s*(?:years?|yrs?)", joined, re.I)

    role = ""
    role_terms = ["software engineer", "software developer", "python developer", "java developer", "data analyst", "data scientist", "web developer", "full stack developer", "frontend developer", "backend developer", "machine learning engineer", "intern"]
    for term in role_terms:
        if term in lower_text:
            role = term.title()
            break

    location = ""
    for line in lines[:30]:
        if re.search(r"\b(Hyderabad|Bengaluru|Bangalore|Chennai|Mumbai|Pune|Delhi|Noida|Kolkata|India)\b", line, re.I):
            location = line[:100]
            break

    return {
        "full_name": full_name,
        "email": email_match.group(0) if email_match else "",
        "phone": phone_match.group(0) if phone_match else "",
        "location": location,
        "current_role": role,
        "total_experience": f"{experience_match.group(1)} years" if experience_match else "",
        "technical_skills": ", ".join(skills_found),
        "education": "\n".join(education_lines[:8]),
        "certifications": "\n".join(certification_lines[:8]),
    }


def render_resume_center():
    st.markdown('<div class="eyebrow">RESUME INTELLIGENCE</div>', unsafe_allow_html=True)
    st.title("Resume & profile review")
    st.caption("Upload your latest resume. The portal will read the document text and prepare candidate details for your review.")

    left, right = st.columns([1.2, 0.8])
    with left:
        st.markdown("### Upload your resume")
        st.markdown('<div class="panel"><div class="panel-title">Accepted file formats</div><p class="muted">PDF · DOC · DOCX &nbsp; | &nbsp; Maximum size: 5 MB</p></div>', unsafe_allow_html=True)
        uploaded = st.file_uploader("Choose resume file", type=["pdf", "doc", "docx"], key="candidate_resume_uploader")
        if uploaded:
            if uploaded.size > MAX_RESUME_SIZE:
                st.error("This file is larger than 5 MB. Please upload a smaller resume.")
            else:
                digest = hashlib.sha256(uploaded.getvalue()).hexdigest()
                if st.session_state.get("resume_upload_identity") != digest:
                    st.session_state.resume_file_name = uploaded.name
                    st.session_state.resume_file_bytes = uploaded.getvalue()
                    st.session_state.resume_upload_identity = digest
                    st.session_state.resume_review_data = {}
                    st.session_state.resume_review_confirmed = False
                    try:
                        extracted_text = extract_document_text(uploaded)
                        st.session_state.resume_extracted_text = extracted_text
                        st.session_state.resume_review_data = extract_candidate_fields(extracted_text)
                        st.session_state.resume_parse_error = ""
                    except Exception as exc:
                        st.session_state.resume_extracted_text = ""
                        st.session_state.resume_review_data = {}
                        st.session_state.resume_parse_error = str(exc)
                st.success(f"Resume received: {uploaded.name}")
                st.markdown(f'<div class="panel"><div class="panel-title">{uploaded.name}</div><p class="muted">{uploaded.size / 1024:.1f} KB · File received in this session</p><span class="pill">UPLOADED</span></div>', unsafe_allow_html=True)
    with right:
        st.markdown("### Upload checklist")
        st.markdown('<div class="panel"><p>✓ Use a readable document</p><p>✓ Include your latest skills and experience</p><p>✓ Check your phone and email details</p><p>✓ Review every detected field before confirming</p></div>', unsafe_allow_html=True)

    if st.session_state.get("resume_file_name"):
        st.divider()
        st.markdown("### Extracted profile information")
        parse_error = st.session_state.get("resume_parse_error", "")
        if parse_error:
            st.error(parse_error)
        else:
            review = st.session_state.get("resume_review_data", {})
            if not review or not any(str(value).strip() for value in review.values()):
                st.warning("The document was uploaded, but no readable text or candidate details could be detected. Please check the document and try another file.")
            else:
                st.caption("These values were detected from the uploaded document. Fields not found in the resume are left blank; please verify everything.")
                with st.form("resume_extracted_profile_review"):
                    c1, c2 = st.columns(2)
                    with c1:
                        full_name = st.text_input("Full name", value=review.get("full_name", ""))
                        email = st.text_input("Email address", value=review.get("email", ""))
                        phone = st.text_input("Phone number", value=review.get("phone", ""))
                        location = st.text_input("Location", value=review.get("location", ""))
                        current_role = st.text_input("Current / target role", value=review.get("current_role", ""))
                    with c2:
                        experience = st.text_input("Total experience", value=review.get("total_experience", ""))
                        education = st.text_area("Education", value=review.get("education", ""), height=110)
                        certifications = st.text_area("Certifications", value=review.get("certifications", ""), height=110)
                    skills = st.text_area("Technical skills", value=review.get("technical_skills", ""), height=110)
                    confirm = st.form_submit_button("Confirm corrected details", type="primary", use_container_width=True)
                if confirm:
                    if not full_name.strip():
                        st.error("Full name is required before confirmation.")
                    elif email.strip() and not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email.strip()):
                        st.error("Enter a valid email address or leave it blank if the resume does not contain one.")
                    else:
                        st.session_state.resume_review_data = {
                            "full_name": full_name.strip(), "email": email.strip(), "phone": phone.strip(),
                            "location": location.strip(), "current_role": current_role.strip(),
                            "total_experience": experience.strip(), "education": education.strip(),
                            "certifications": certifications.strip(), "technical_skills": skills.strip()
                        }
                        st.session_state.resume_review_confirmed = True
                        st.success("Your corrected details are confirmed in this demo session. They have not yet been sent to FastAPI or a database.")
                if st.session_state.get("resume_review_confirmed"):
                    st.success("Candidate review status: Confirmed")

        with st.expander("View extracted document text"):
            extracted_text = st.session_state.get("resume_extracted_text", "")
            if extracted_text.strip():
                st.text_area("Document text", value=extracted_text, height=260, disabled=True)
            else:
                st.caption("No document text is available.")
