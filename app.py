import re

from pathlib import Path



import streamlit as st

import Candidate_Portal

import resume_module



st.set_page_config(
    page_title="BlueTip AI | Candidate Portal",
    page_icon="bluetipai_icon.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)



SVG_LOGO = r"""
<svg xmlns="http://www.w3.org/2000/svg" width="520" height="120" viewBox="0 0 520 120" role="img" aria-labelledby="title desc">
  <title id="title">BlueTip AI</title>
  <desc id="desc">BlueTip AI logo with a geometric blue and cyan technology mark and wordmark.</desc>
  <defs>
    <linearGradient id="bt-gradient" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#69A7FF"/>
      <stop offset="55%" stop-color="#477CF0"/>
      <stop offset="100%" stop-color="#46D6D0"/>
    </linearGradient>
    <linearGradient id="bt-text" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#F5F8FF"/>
      <stop offset="100%" stop-color="#BFD5FF"/>
    </linearGradient>
    <filter id="bt-glow" x="-40%" y="-40%" width="180%" height="180%">
      <feGaussianBlur stdDeviation="5" result="blur"/>
      <feMerge><feMergeNode in="blur"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g transform="translate(12 10)">
    <path d="M50 4 L91 27 L91 73 L50 96 L9 73 L9 27 Z" fill="#101D33" stroke="url(#bt-gradient)" stroke-width="3"/>
    <path d="M30 31 H52 C66 31 72 38 72 48 C72 58 66 65 52 65 H30 Z" fill="none" stroke="url(#bt-gradient)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/>
    <path d="M48 31 L48 65 M48 48 H70" fill="none" stroke="#EAF3FF" stroke-width="5" stroke-linecap="round"/>
    <circle cx="75" cy="25" r="6" fill="#46D6D0" filter="url(#bt-glow)"/>
    <path d="M76 25 L85 16" stroke="#46D6D0" stroke-width="3" stroke-linecap="round"/>
  </g>
  <text x="125" y="66" font-family="Manrope, Inter, Arial, sans-serif" font-size="48" font-weight="800" letter-spacing="-1.8" fill="url(#bt-text)">BlueTip</text>
  <text x="310" y="66" font-family="Manrope, Inter, Arial, sans-serif" font-size="48" font-weight="800" letter-spacing="-1.8" fill="#62A5FF">AI</text>
  <text x="128" y="91" font-family="Inter, Arial, sans-serif" font-size="12" font-weight="600" letter-spacing="3.2" fill="#91A8C8">INTELLIGENT TALENT PLATFORM</text>
</svg>
"""



CUSTOM_CSS = """

<style>

@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

:root { --bg:#080d18; --panel:#101827; --panel2:#131f31; --line:rgba(148,163,184,.16); --muted:#91a0b7; --text:#eef4ff; --blue:#4f8cff; --cyan:#42d6d0; }

.stApp { background: radial-gradient(circle at 75% -10%, rgba(48,91,170,.22), transparent 34%), var(--bg); color:var(--text); font-family:'DM Sans',sans-serif; }

header[data-testid="stHeader"] { background:rgba(8,13,24,.55); }

footer {visibility:hidden;}

.block-container { padding-top:1.8rem; padding-bottom:3rem; max-width:1440px; }

h1,h2,h3,h4 { font-family:'Manrope',sans-serif !important; letter-spacing:-.035em; }

h1 { font-weight:800 !important; }

p, label, .stMarkdown { color:#dce6f5; }

[data-testid="stSidebar"] { background:linear-gradient(180deg,#0e1727 0%,#0a1220 100%); border-right:1px solid var(--line); }

[data-testid="stSidebar"] > div:first-child { padding-top:1.1rem; }

[data-testid="stSidebar"] [data-testid="stRadio"] > div { gap:.38rem; }

[data-testid="stSidebar"] [data-testid="stRadio"] label { border:1px solid transparent; border-radius:12px; padding:.62rem .72rem; transition:all .2s ease; }

[data-testid="stSidebar"] [data-testid="stRadio"] label:hover { background:rgba(79,140,255,.10); border-color:rgba(79,140,255,.18); }

[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) { background:linear-gradient(100deg,rgba(79,140,255,.22),rgba(66,214,208,.08)); border:1px solid rgba(79,140,255,.28); }

.stButton > button, .stFormSubmitButton > button { border-radius:11px; min-height:2.65rem; font-weight:700; border:1px solid rgba(148,163,184,.22); transition:all .2s ease; }

.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] { background:linear-gradient(105deg,#3979ed,#5268e8); border:0; color:white; box-shadow:0 8px 24px rgba(55,105,220,.22); }

.stButton > button:hover, .stFormSubmitButton > button:hover { border-color:#5b9bff; transform:translateY(-1px); }

.stTextInput input,.stTextArea textarea,.stDateInput input,.stNumberInput input,.stSelectbox div[data-baseweb="select"] > div { background:#0d1727 !important; border:1px solid rgba(148,163,184,.22) !important; border-radius:10px !important; color:#f3f7ff !important; }

[data-testid="stFileUploader"] { background:rgba(18,31,49,.62); border:1px dashed rgba(91,155,255,.42); border-radius:14px; padding:.55rem; }

[data-testid="stMetric"] { background:linear-gradient(145deg,rgba(19,31,49,.94),rgba(13,23,39,.94)); border:1px solid var(--line); padding:17px 18px; border-radius:15px; }

[data-testid="stMetricLabel"] { color:#91a0b7 !important; }

[data-testid="stMetricValue"] { color:#f2f7ff !important; font-family:'Manrope',sans-serif; }

div[data-testid="stTabs"] button { color:#aebbd0; font-weight:700; }

div[data-testid="stTabs"] button[aria-selected="true"] { color:#72a9ff; }

hr { border-color:var(--line); }

.hero { padding:3.4rem 2.8rem; border:1px solid rgba(119,159,230,.20); border-radius:25px; background:radial-gradient(circle at 85% 15%,rgba(66,214,208,.16),transparent 25%),linear-gradient(120deg,rgba(24,47,82,.96),rgba(13,25,44,.96)); box-shadow:0 24px 80px rgba(0,0,0,.22); }

.eyebrow { color:#78b7ff; font-size:.76rem; font-weight:800; text-transform:uppercase; letter-spacing:.16em; }

.hero h1 { font-size:clamp(2.1rem,4vw,3.55rem); line-height:1.08; margin:.7rem 0; color:#f5f8ff; }

.hero p { max-width:690px; color:#b5c5db; font-size:1.05rem; line-height:1.7; }

.panel { background:linear-gradient(145deg,rgba(19,31,49,.95),rgba(13,22,37,.95)); border:1px solid var(--line); border-radius:17px; padding:1.2rem 1.35rem; margin-bottom:.8rem; }

.panel-title { color:#f2f6ff; font-family:'Manrope',sans-serif; font-weight:800; font-size:1.03rem; }

.muted { color:#91a0b7; }

.pill { display:inline-block; padding:.32rem .68rem; border-radius:999px; background:rgba(66,214,208,.10); border:1px solid rgba(66,214,208,.24); color:#78e2dc; font-size:.76rem; font-weight:700; }

.login-wrap { max-width:560px; margin:1rem auto; }

.small-note { color:#91a0b7; font-size:.84rem; }

[data-testid="stAlert"] { border-radius:12px; }

</style>

"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)







def render_logo(width=190):
    """Render the inline SVG logo at the width requested by each page."""
    st.markdown(
        f"""
        <div style="width:{width}px; max-width:100%; margin:0; padding:0; line-height:0;">
            <style>
                .bluetip-inline-logo svg {{
                    display:block;
                    width:100% !important;
                    height:auto !important;
                    max-width:100% !important;
                }}
            </style>
            <div class="bluetip-inline-logo">{SVG_LOGO}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


def init_state():

    defaults = {

        "logged_in": False,

        "candidate_email": "",

        "view": "landing",

        "candidate_navigation": "overview",

        "registered_users": {"candidate@bluetipai.com": "Bluetip@123"},

        "profile_data": {},

        "education_history": [],

        "projects_history": [],

        "resume_file_name": "",

        "resume_file_bytes": None,

        "resume_review_data": {},

        "resume_review_confirmed": False,

        "resume_extracted_text": "",

        "resume_parse_error": "",

    }

    for key, value in defaults.items():

        if key not in st.session_state:

            st.session_state[key] = value





init_state()





def logout():

    st.session_state.logged_in = False

    st.session_state.view = "login"

    st.session_state.candidate_email = ""

    st.session_state.pop("candidate_navigation", None)

    st.session_state.pop("candidate_resume_uploader", None)





def render_landing():

    top1, top2, top3 = st.columns([6, 1.2, 1.4])

    with top1:

        render_logo(380)  # Home page logo: 380px

    with top2:

        st.write("")

        st.caption("CANDIDATE PORTAL")

    with top3:

        if st.button("Sign in  →", type="primary", use_container_width=True):

            st.session_state.view = "login"

            st.rerun()



    st.markdown("""

    <div class="hero">

      <div class="eyebrow">Your next opportunity starts here</div>

      <h1>Showcase your skills.<br>Move your career forward.</h1>

      <p>Manage your candidate profile, share your latest resume and complete technical assessments through one secure candidate workspace.</p>

      <span class="pill">Profile · Resume intelligence · Assessments</span>

    </div>

    """, unsafe_allow_html=True)

    st.write("")

    st.markdown("### Everything you need, in one place")

    a, b, c = st.columns(3)

    cards = [

        ("01", "Build your profile", "Keep your contact details, education, experience and projects up to date."),

        ("02", "Verify your resume", "Upload your resume and review extracted information before confirming it."),

        ("03", "Complete assessments", "Access assigned assessments and track your progress from your dashboard."),

    ]

    for col, (num, title, desc) in zip([a, b, c], cards):

        with col:

            st.markdown(f'<div class="panel"><div class="eyebrow">{num}</div><div class="panel-title">{title}</div><p class="muted">{desc}</p></div>', unsafe_allow_html=True)

    st.caption("BlueTip AI · Candidate workspace")





def render_auth():

    left, center, right = st.columns([1, 1.35, 1])

    with center:

        render_logo(190)  # Login page logo: 190px

        st.markdown('<div class="login-wrap">', unsafe_allow_html=True)

        st.markdown("## Welcome to BlueTip AI")

        st.caption("Sign in to continue to your candidate workspace.")

        login_tab, signup_tab = st.tabs(["Sign in", "Create account"])

        with login_tab:

            with st.form("candidate_login_form"):

                email = st.text_input("Email address", placeholder="you@example.com")

                password = st.text_input("Password", type="password", placeholder="Enter your password")

                submitted = st.form_submit_button("Sign in to portal", type="primary", use_container_width=True)

            if submitted:

                users = st.session_state.registered_users

                clean_email = email.strip().lower()

                if clean_email in users and users[clean_email] == password:

                    st.session_state.logged_in = True

                    st.session_state.candidate_email = clean_email

                    st.session_state.view = "dashboard"

                    st.session_state.candidate_navigation = "overview"

                    st.rerun()

                else:

                    st.error("Email address or password is incorrect.")

            st.info("Demo login: candidate@bluetipai.com  |  Password: Bluetip@123")

        with signup_tab:

            with st.form("candidate_signup_form"):

                new_email = st.text_input("Email address", placeholder="you@example.com")

                new_password = st.text_input("Create password", type="password", help="At least 8 characters, uppercase, lowercase, number and special character.")

                confirm_password = st.text_input("Confirm password", type="password")

                create = st.form_submit_button("Create candidate account", type="primary", use_container_width=True)

            if create:

                clean_email = new_email.strip().lower()

                password_pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"

                if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", clean_email):

                    st.error("Enter a valid email address.")

                elif clean_email in st.session_state.registered_users:

                    st.error("An account with this email already exists.")

                elif not re.fullmatch(password_pattern, new_password):

                    st.error("Password must contain at least 8 characters, uppercase, lowercase, number and special character.")

                elif new_password != confirm_password:

                    st.error("Passwords do not match.")

                else:

                    st.session_state.registered_users[clean_email] = new_password

                    st.success("Account created. You can now sign in.")

        st.markdown('<p class="small-note">Demo mode · Authentication is currently stored in Streamlit session state. Connect FastAPI authentication before production use.</p>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        if st.button("← Back to home", use_container_width=True):

            st.session_state.view = "landing"

            st.rerun()





def render_dashboard_overview():

    profile = st.session_state.get("profile_data", {})

    has_profile = bool(profile.get("first_name") and profile.get("last_name"))

    has_resume = bool(st.session_state.get("resume_file_name"))

    resume_confirmed = bool(st.session_state.get("resume_review_confirmed"))

    st.markdown('<div class="eyebrow">CANDIDATE WORKSPACE</div>', unsafe_allow_html=True)

    st.title(f"Welcome{', ' + profile.get('first_name', '') if profile.get('first_name') else ''} ")

    st.caption("Your personal space to manage your profile, resume and candidate journey.")

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("Profile", "Started" if has_profile else "Not started")

    m2.metric("Resume", "Uploaded" if has_resume else "Pending")

    m3.metric("AI review", "Confirmed" if resume_confirmed else ("Review needed" if has_resume else "Not started"))

    m4.metric("Assessments", "No assignment")

    st.write("")

    st.markdown("### Your next steps")

    step_cols = st.columns(2)

    with step_cols[0]:

        st.markdown('<div class="panel"><div class="eyebrow">STEP 01</div><div class="panel-title">Complete your candidate profile</div><p class="muted">Add your personal details, academic history, experience and projects.</p></div>', unsafe_allow_html=True)

        st.button(

            "Open my profile →", type="primary", use_container_width=True,

            on_click=_set_candidate_navigation, args=("profile",), key="open_candidate_profile"

        )

    with step_cols[1]:

        st.markdown('<div class="panel"><div class="eyebrow">STEP 02</div><div class="panel-title">Upload and verify your resume</div><p class="muted">Upload a PDF, DOC or DOCX file and review extracted candidate information.</p></div>', unsafe_allow_html=True)

        st.button(

            "Go to resume centre →", use_container_width=True,

            on_click=_set_candidate_navigation, args=("resume",), key="open_candidate_resume"

        )

    st.markdown("### Candidate journey")

    journey = st.columns(4)

    journey_items = [("Profile", has_profile), ("Resume", has_resume), ("AI verification", resume_confirmed), ("Assessment", False)]

    for col, (label, complete) in zip(journey, journey_items):

        with col:

            st.markdown(f'<div class="panel"><span class="pill">{"COMPLETED" if complete else "UP NEXT"}</span><p class="panel-title">{label}</p></div>', unsafe_allow_html=True)





def _set_candidate_navigation(destination):

    st.session_state.candidate_navigation = destination





def render_app_shell():

    nav = {

        "overview": "◈  Overview",

        "profile": "◎  My profile",

        "resume": "▤  Resume & AI review",

        "assessments": "▣  Assessments",

        "applications": "◷  Application status",

        "onboarding": "↗  Onboarding",

    }

    if st.session_state.candidate_navigation not in nav:

        st.session_state.candidate_navigation = "overview"



    with st.sidebar:

        render_logo(205)  # Sidebar logo: 205px

        st.markdown('<div class="eyebrow">CANDIDATE WORKSPACE</div>', unsafe_allow_html=True)

        st.write("")

        selected = st.radio("Workspace navigation", list(nav), format_func=nav.get, key="candidate_navigation", label_visibility="collapsed")

        st.divider()

        email = st.session_state.candidate_email

        initials = (email.split("@")[0][:2] if email else "CA").upper()

        st.markdown(f'<div class="panel"><div class="pill">SIGNED IN</div><p class="panel-title">{initials} · Candidate</p><p class="small-note">{email}</p></div>', unsafe_allow_html=True)

        st.button("↪  Sign out", use_container_width=True, on_click=logout)

        st.caption("BlueTip AI · Candidate Portal")



    if selected == "overview":

        render_dashboard_overview()

    elif selected == "profile":

        Candidate_Portal.render_candidate_profile()

    elif selected == "resume":

        resume_module.render_resume_center()

    elif selected == "assessments":

        st.markdown('<div class="eyebrow">ASSESSMENT CENTRE</div>', unsafe_allow_html=True)

        st.title("Your assessments")

        st.info("No assessment invitations are available in demo mode. Assigned assessments will appear here after the assessment API is connected.")

    elif selected == "applications":

        st.markdown('<div class="eyebrow">CANDIDATE JOURNEY</div>', unsafe_allow_html=True)

        st.title("Application status")

        st.info("Your application updates will appear here when the backend provides application records.")

    elif selected == "onboarding":

        st.markdown('<div class="eyebrow">GETTING STARTED</div>', unsafe_allow_html=True)

        st.title("Onboarding")

        st.info("Onboarding tasks will appear here when they are assigned to you.")





if st.session_state.logged_in:

    render_app_shell()

elif st.session_state.view == "login":

    render_auth()

else:

    render_landing()
