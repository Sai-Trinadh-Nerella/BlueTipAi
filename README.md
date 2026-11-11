# BlueTip AI Candidate Portal

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Demo login

- Email: `candidate@bluetipai.com`
- Password: `Bluetip@123`

## Implemented in this frontend build

- Candidate landing page and sign-in/sign-up UI
- Candidate dashboard with redesigned sidebar navigation
- Candidate profile editing UI for personal, address, education, experience and project details
- Resume upload interface for PDF, DOC and DOCX (maximum 5 MB)
- Editable resume-extraction correction screen with clearly labelled sample data

## Important integration notes

This is a Streamlit frontend prototype. Authentication, profile persistence, file storage and actual AI resume parsing are not connected to FastAPI yet. The sample extraction data is only for previewing the UI workflow. Do not use the demo credentials or session-state password storage in production.

The original profile implementation is retained in `task1_module_legacy.py` for reference.
