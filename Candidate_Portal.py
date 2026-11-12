import re
from datetime import date, datetime
import streamlit as st


def initialize_profile():
    if "profile_data" not in st.session_state:
        st.session_state.profile_data = {}
    if "education_history" not in st.session_state:
        st.session_state.education_history = []
    if "projects_history" not in st.session_state:
        st.session_state.projects_history = []


def _cancel_profile_edit():
    st.session_state.candidate_navigation = "overview"


def _clear_invalid_field(key):
    invalid_fields = st.session_state.get("profile_invalid_fields", [])
    if key in invalid_fields:
        st.session_state.profile_invalid_fields = [
            field for field in invalid_fields if field != key
        ]


def _sanitize_digit_field(key, max_digits):
    value = st.session_state.get(key, "")
    st.session_state[key] = re.sub(r"\D", "", str(value))[:max_digits]
    _clear_invalid_field(key)


def render_candidate_profile():
    initialize_profile()
    profile = st.session_state.profile_data
    email = st.session_state.get("candidate_email", "")
    st.markdown('<div class="eyebrow">PROFILE MANAGEMENT</div>', unsafe_allow_html=True)
    st.title("My candidate profile")
    st.caption("Keep your information accurate so recruiters can understand your skills and experience.")
    if st.session_state.get("profile_invalid_fields"):
        st.error("Please complete all required fields before saving your profile.")

    first = profile.get("first_name", "")
    last = profile.get("last_name", "")
    completeness_fields = [first, last, profile.get("phone", ""), profile.get("city", ""), profile.get("skills", "")]
    completion = round(sum(bool(str(x).strip()) for x in completeness_fields) / len(completeness_fields) * 100)
    c1, c2, c3 = st.columns([1, 1, 2])
    c1.metric("Profile completion", f"{completion}%")
    c2.metric("Education records", len(st.session_state.education_history))
    c3.metric("Projects added", len(st.session_state.projects_history))
    st.progress(completion / 100)

    with st.container(border=True):
        st.markdown("#### Personal and contact information")
        st.caption("Fields marked * are required. Your account email is your login identity.")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("First name *", value=profile.get("first_name", ""), placeholder="Enter first name", key="personal_first_name", on_change=_clear_invalid_field, args=("personal_first_name",))
            st.text_input("Account email *", value=email, disabled=True, key="personal_email")
            phone_default = re.sub(r"\D", "", str(profile.get("phone", "")))[:10]
            phone = st.text_input("Phone number *", value=phone_default, placeholder="10-digit mobile number", type="phone", key="personal_phone", on_change=_sanitize_digit_field, args=("personal_phone", 10))
            phone_digit_count = len(re.sub(r"\D", "", phone))
            if phone_digit_count:
                st.caption(f"{phone_digit_count}/10 digits")
            dob_default = profile.get("date_of_birth")
            if isinstance(dob_default, str):
                try:
                    dob_default = date.fromisoformat(dob_default)
                except ValueError:
                    dob_default = None
            if (
                not isinstance(dob_default, date)
                or dob_default < date(1900, 1, 1)
                or dob_default > date.today()
            ):
                dob_default = None
            dob = st.date_input(
                "Date of birth *",
                value=dob_default,
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                key="personal_date_of_birth",
                format="DD/MM/YYYY",
                help="Enter a date as DD/MM/YYYY, or choose it from the calendar.",
                on_change=_clear_invalid_field,
                args=("personal_date_of_birth",),
            )
            st.caption("For older years, type the full date as DD/MM/YYYY or scroll the year list.")
        with col2:
            last_name = st.text_input("Last name *", value=profile.get("last_name", ""), placeholder="Enter last name", key="personal_last_name", on_change=_clear_invalid_field, args=("personal_last_name",))
            gender_options = ["Select", "Female", "Male", "Non-binary", "Prefer not to say"]
            old_gender = profile.get("gender", "Select")
            gender = st.selectbox("Gender *", gender_options, index=gender_options.index(old_gender) if old_gender in gender_options else 0, key="personal_gender", on_change=_clear_invalid_field, args=("personal_gender",))
            city = st.text_input("City / town *", value=profile.get("city", ""), key="personal_city", on_change=_clear_invalid_field, args=("personal_city",))
            state = st.text_input("State *", value=profile.get("state", ""), key="personal_state", on_change=_clear_invalid_field, args=("personal_state",))
        address1 = st.text_input("Address line 1 *", value=profile.get("address1", ""), key="personal_address1", on_change=_clear_invalid_field, args=("personal_address1",))
        address2 = st.text_input("Address line 2 (optional)", value=profile.get("address2", ""), key="personal_address2")
        col3, col4 = st.columns(2)
        with col3:
            pincode_default = re.sub(r"\D", "", str(profile.get("pincode", "")))[:6]
            pincode = st.text_input("PIN code *", value=pincode_default, placeholder="6-digit PIN code", key="personal_pincode", on_change=_sanitize_digit_field, args=("personal_pincode", 6))
            pincode_digit_count = len(re.sub(r"\D", "", pincode))
            if pincode_digit_count:
                st.caption(f"{pincode_digit_count}/6 digits")
        with col4:
            country = st.text_input("Country *", value=profile.get("country", ""), key="personal_country_input", on_change=_clear_invalid_field, args=("personal_country_input",))
        skills = st.text_area("Technical skills *", value=profile.get("skills", ""), placeholder="Python, SQL, FastAPI, Streamlit...", height=100, key="personal_skills", on_change=_clear_invalid_field, args=("personal_skills",))

    with st.container(border=True):
        st.markdown("#### Educational background")
        if st.session_state.education_history:
            for index, item in enumerate(st.session_state.education_history):
                with st.expander(f"{item.get('Level', 'Education')} · {item.get('Institution', '')}"):
                    st.write(f"**Qualification:** {item.get('Board/Degree/Stream', '-')}")
                    st.write(f"**Score:** {item.get('Score', '-')}")
                    st.write(f"**Years:** {item.get('Joining Year', '-')} – {item.get('Passing/Completion Year', '-')}")
                    st.write(f"**Status:** {item.get('Status', '-')}")
                    if st.button("Remove record", key=f"remove_education_{index}"):
                        st.session_state.education_history.pop(index)
                        st.rerun()

        levels = ["High School", "Intermediate", "Diploma", "Bachelor's Degree", "Master's Degree", "Ph.D."]
        selected_level = st.selectbox("Qualification *", levels, key="education_level_selection")
        st.caption(f"Enter the details for your {selected_level} qualification.")
        edu_key = f"education_form_{len(st.session_state.education_history)}_{selected_level.lower().replace(' ', '_').replace(chr(39), '')}"

        institution_labels = {
            "High School": "School name",
            "Intermediate": "College name",
            "Diploma": "College / Institution",
            "Bachelor's Degree": "College / University",
            "Master's Degree": "University",
            "Ph.D.": "University / Research institution"
        }
        institution = st.text_input(f"{institution_labels[selected_level]} *", key=f"{edu_key}_institution", on_change=_clear_invalid_field, args=(f"{edu_key}_institution",))

        other_value = ""
        if selected_level == "High School":
            board_options = ["CBSE", "ICSE", "State Board", "IGCSE", "Other"]
            board = st.selectbox("Education Board *", board_options, key=f"{edu_key}_board", on_change=_clear_invalid_field, args=(f"{edu_key}_board",))
            if board == "Other":
                other_value = st.text_input("Enter education board *", key=f"{edu_key}_board_other", on_change=_clear_invalid_field, args=(f"{edu_key}_board_other",))
            qualification = other_value if board == "Other" else board

        elif selected_level == "Intermediate":
            board_options = ["CBSE", "State Board", "ISC", "Other"]
            col_a, col_b = st.columns(2)
            with col_a:
                board = st.selectbox("Education Board *", board_options, key=f"{edu_key}_board", on_change=_clear_invalid_field, args=(f"{edu_key}_board",))
            with col_b:
                stream_options = ["MPC", "BiPC", "MEC", "CEC", "HEC", "Other"]
                stream = st.selectbox("Stream *", stream_options, key=f"{edu_key}_stream", on_change=_clear_invalid_field, args=(f"{edu_key}_stream",))
            board_other = st.text_input("Enter education board *", key=f"{edu_key}_board_other", on_change=_clear_invalid_field, args=(f"{edu_key}_board_other",)) if board == "Other" else ""
            stream_other = st.text_input("Enter stream *", key=f"{edu_key}_stream_other", on_change=_clear_invalid_field, args=(f"{edu_key}_stream_other",)) if stream == "Other" else ""
            qualification = f"{board_other or board} - {stream_other or stream}"

        elif selected_level == "Diploma":
            col_a, col_b = st.columns(2)
            with col_a:
                branch_options = ["CSE", "EEE", "ECE", "Mechanical", "Civil", "IT", "Automobile", "Other"]
                branch = st.selectbox("Diploma Branch *", branch_options, key=f"{edu_key}_branch", on_change=_clear_invalid_field, args=(f"{edu_key}_branch",))
            with col_b:
                specialization_options = ["Artificial Intelligence", "Machine Learning", "Data Science", "Cyber Security", "Cloud Computing", "VLSI", "Embedded Systems", "Other", "Not applicable"]
                specialization = st.selectbox("Specialization *", specialization_options, key=f"{edu_key}_specialization", on_change=_clear_invalid_field, args=(f"{edu_key}_specialization",))
            branch_other = st.text_input("Enter diploma branch *", key=f"{edu_key}_branch_other", on_change=_clear_invalid_field, args=(f"{edu_key}_branch_other",)) if branch == "Other" else ""
            specialization_other = st.text_input("Enter specialization *", key=f"{edu_key}_specialization_other", on_change=_clear_invalid_field, args=(f"{edu_key}_specialization_other",)) if specialization == "Other" else ""
            qualification = f"{branch_other or branch} - {specialization_other or specialization}"

        elif selected_level == "Bachelor's Degree":
            col_a, col_b = st.columns(2)
            with col_a:
                degree_options = ["CSE", "IT", "EEE", "ECE", "Mechanical Engineering", "Civil Engineering", "Chemical Engineering", "Biotechnology", "B.Sc", "BCA", "B.Com", "B.A", "Other"]
                degree = st.selectbox("Degree / Branch *", degree_options, key=f"{edu_key}_degree", on_change=_clear_invalid_field, args=(f"{edu_key}_degree",))
            with col_b:
                specialization_options = ["Artificial Intelligence", "Machine Learning", "Data Science", "Cyber Security", "Cloud Computing", "Software Engineering", "Web Development", "VLSI", "Embedded Systems", "Finance", "Marketing", "General", "Other", "Not applicable"]
                specialization = st.selectbox("Specialization *", specialization_options, key=f"{edu_key}_specialization", on_change=_clear_invalid_field, args=(f"{edu_key}_specialization",))
            degree_other = st.text_input("Enter degree / branch *", key=f"{edu_key}_degree_other", on_change=_clear_invalid_field, args=(f"{edu_key}_degree_other",)) if degree == "Other" else ""
            specialization_other = st.text_input("Enter specialization *", key=f"{edu_key}_specialization_other", on_change=_clear_invalid_field, args=(f"{edu_key}_specialization_other",)) if specialization == "Other" else ""
            qualification = f"{degree_other or degree} - {specialization_other or specialization}"

        elif selected_level == "Master's Degree":
            col_a, col_b = st.columns(2)
            with col_a:
                degree_options = ["M.Tech", "M.E", "M.S", "M.Sc", "MCA", "MBA", "M.Com", "M.A", "Other"]
                degree = st.selectbox("Degree / Branch *", degree_options, key=f"{edu_key}_degree", on_change=_clear_invalid_field, args=(f"{edu_key}_degree",))
            with col_b:
                specialization_options = ["Computer Science", "Artificial Intelligence", "Machine Learning", "Data Science", "Cyber Security", "Cloud Computing", "Electronics", "Electrical Engineering", "Mechanical Engineering", "Finance", "Human Resources", "Marketing", "Other"]
                specialization = st.selectbox("Specialization *", specialization_options, key=f"{edu_key}_specialization", on_change=_clear_invalid_field, args=(f"{edu_key}_specialization",))
            degree_other = st.text_input("Enter degree *", key=f"{edu_key}_degree_other", on_change=_clear_invalid_field, args=(f"{edu_key}_degree_other",)) if degree == "Other" else ""
            specialization_other = st.text_input("Enter specialization *", key=f"{edu_key}_specialization_other", on_change=_clear_invalid_field, args=(f"{edu_key}_specialization_other",)) if specialization == "Other" else ""
            qualification = f"{degree_other or degree} - {specialization_other or specialization}"

        else:
            research_options = ["Computer Science", "Artificial Intelligence", "Machine Learning", "Data Science", "Electrical Engineering", "Electronics", "Mechanical Engineering", "Civil Engineering", "Physics", "Chemistry", "Mathematics", "Other"]
            research_area = st.selectbox("Research area / Specialization *", research_options, key=f"{edu_key}_research", on_change=_clear_invalid_field, args=(f"{edu_key}_research",))
            research_other = st.text_input("Enter research area *", key=f"{edu_key}_research_other", on_change=_clear_invalid_field, args=(f"{edu_key}_research_other",)) if research_area == "Other" else ""
            qualification = research_other or research_area

        col1, col2 = st.columns(2)
        with col1:
            score = st.text_input("Score / CGPA / Percentage *", key=f"{edu_key}_score", on_change=_clear_invalid_field, args=(f"{edu_key}_score",))
            start_year = st.number_input("Joining year *", min_value=1980, max_value=datetime.now().year + 5, value=None, placeholder="Enter joining year", key=f"{edu_key}_start_input")
        with col2:
            status = st.selectbox("Status *", ["Completed", "Ongoing", "Expected"], key=f"{edu_key}_status")
            end_year = st.number_input("Passing / expected year *", min_value=1980, max_value=datetime.now().year + 8, value=None, placeholder="Enter passing year", key=f"{edu_key}_end_input")
        if st.button("＋ Add education", key=f"{edu_key}_add", use_container_width=True):
            qualification_complete = bool(qualification.strip())
            if selected_level == "High School":
                qualification_complete = board != "Other" or bool(other_value.strip())
            elif selected_level == "Intermediate":
                qualification_complete = (board != "Other" or bool(board_other.strip())) and (stream != "Other" or bool(stream_other.strip()))
            elif selected_level == "Diploma":
                qualification_complete = (branch != "Other" or bool(branch_other.strip())) and (specialization != "Other" or bool(specialization_other.strip()))
            elif selected_level in ["Bachelor's Degree", "Master's Degree"]:
                qualification_complete = (degree != "Other" or bool(degree_other.strip())) and (specialization != "Other" or bool(specialization_other.strip()))
            elif selected_level == "Ph.D.":
                qualification_complete = research_area != "Other" or bool(research_other.strip())
            if not institution.strip() or not qualification_complete or not score.strip():
                st.error("Complete all required education details, including any Other fields and your score.")
            elif start_year is None or end_year is None:
                st.error("Enter both the joining year and passing / expected year.")
            elif end_year < start_year:
                st.error("Passing year cannot be earlier than joining year.")
            else:
                st.session_state.education_history.append({
                    "Level": selected_level, "Institution": institution.strip(),
                    "Board/Degree/Stream": qualification.strip(), "Score": score.strip() or "-",
                    "Joining Year": int(start_year), "Passing/Completion Year": int(end_year), "Status": status
                })
                st.success("Education record added.")
                st.rerun()

    with st.container(border=True):
        st.markdown("#### Professional experience")
        experience_type = st.radio(
            "Experience level *", ["Fresher", "Experienced"], horizontal=True,
            index=1 if profile.get("experience_type") == "Experienced" else 0,
            key="candidate_experience_type"
        )
        if experience_type == "Experienced":
            col1, col2 = st.columns(2)
            with col1:
                company = st.text_input("Current / previous company *", value=profile.get("company", ""), key="experience_company", on_change=_clear_invalid_field, args=("experience_company",))
                job_role = st.text_input("Current / previous role *", value=profile.get("job_role", ""), key="experience_role", on_change=_clear_invalid_field, args=("experience_role",))
            with col2:
                years = st.number_input("Years of experience *", min_value=0.5, max_value=50.0, value=profile.get("years_experience"), placeholder="Enter years of experience", step=0.5, key="experience_years_input")
                expected_salary = st.text_input("Expected salary (optional)", value=profile.get("expected_salary", ""), key="experience_expected_salary")
            previous_salary = st.text_input("Previous salary (optional)", value=profile.get("previous_salary", ""), key="experience_previous_salary")
        else:
            st.info("As a fresher, you do not need to provide previous company, job role, work experience or previous salary details.")
            expected_salary = st.text_input("Expected salary (optional)", value=profile.get("expected_salary", ""), key="fresher_expected_salary")
            company, job_role, years, previous_salary = "", "", 0.0, ""

    with st.container(border=True):
        st.markdown("#### Projects (optional)")
        st.caption("If you add a project, its title, description and technologies are required.")
        if st.session_state.projects_history:
            for index, project in enumerate(st.session_state.projects_history):
                with st.expander(project.get("Project Title", "Project")):
                    st.write(project.get("Description", ""))
                    st.caption("Technologies: " + project.get("Technologies", ""))
                    if project.get("Link"):
                        st.write(project["Link"])
                    if st.button("Remove project", key=f"remove_project_{index}"):
                        st.session_state.projects_history.pop(index)
                        st.rerun()
        project_key = f"project_form_{len(st.session_state.projects_history)}"
        project_title = st.text_input("Project title", key=f"{project_key}_title")
        project_description = st.text_area("Project description", key=f"{project_key}_description")
        technologies = st.text_input("Technologies used", key=f"{project_key}_technologies")
        project_link = st.text_input("GitHub / project URL (optional)", key=f"{project_key}_link")
        if st.button("＋ Add project", key=f"{project_key}_add", use_container_width=True):
            if not project_title.strip() or not project_description.strip() or not technologies.strip():
                st.error("Project title, description and technologies are required.")
            elif project_link.strip() and not re.fullmatch(r"https?://\S+", project_link.strip()):
                st.error("Enter a valid URL starting with http:// or https://.")
            else:
                st.session_state.projects_history.append({"Project Title": project_title.strip(), "Description": project_description.strip(), "Technologies": technologies.strip(), "Link": project_link.strip()})
                st.success("Project added.")
                st.rerun()

    with st.container(border=True):
        st.markdown("#### Profile photo")
        photo = st.file_uploader("Upload a profile photo (optional)", type=["jpg", "jpeg", "png"], key="candidate_profile_photo", help="JPG or PNG, up to 5 MB.")
        if photo:
            if photo.size > 5 * 1024 * 1024:
                st.error("Profile photo must be 5 MB or smaller.")
            else:
                st.image(photo, width=130)
                st.session_state.profile_photo_name = photo.name
        
    st.divider()
    save_col, cancel_col = st.columns(2)
    with save_col:
        if st.button("Save", type="primary", width="stretch", key="save_candidate_profile"):
            invalid_fields = []
            if isinstance(dob, str):
                try:
                    dob = date.fromisoformat(dob)
                except ValueError:
                    dob = None
            required_text = {
                "personal_first_name": first_name,
                "personal_last_name": last_name,
                "personal_city": city,
                "personal_state": state,
                "personal_address1": address1,
                "personal_country_input": country,
                "personal_skills": skills,
                "personal_email": email,
            }
            invalid_fields.extend(key for key, value in required_text.items() if not value.strip())
            if not re.fullmatch(r"[0-9]{10}", phone.strip()):
                invalid_fields.append("personal_phone")
            if not isinstance(dob, date):
                invalid_fields.append("personal_date_of_birth")
            if gender == "Select":
                invalid_fields.append("personal_gender")
            if not re.fullmatch(r"[0-9]{6}", pincode.strip()):
                invalid_fields.append("personal_pincode")

            if not st.session_state.education_history:
                invalid_fields.extend((f"{edu_key}_institution", f"{edu_key}_score"))
                qualification_keys = {
                    "High School": [f"{edu_key}_board"],
                    "Intermediate": [f"{edu_key}_board", f"{edu_key}_stream"],
                    "Diploma": [f"{edu_key}_branch", f"{edu_key}_specialization"],
                    "Bachelor's Degree": [f"{edu_key}_degree", f"{edu_key}_specialization"],
                    "Master's Degree": [f"{edu_key}_degree", f"{edu_key}_specialization"],
                    "Ph.D.": [f"{edu_key}_research"],
                }
                invalid_fields.extend(qualification_keys[selected_level])
                for other_key in (
                    f"{edu_key}_board_other", f"{edu_key}_stream_other",
                    f"{edu_key}_branch_other", f"{edu_key}_specialization_other",
                    f"{edu_key}_degree_other", f"{edu_key}_research_other",
                ):
                    if other_key in st.session_state:
                        invalid_fields.append(other_key)

            if experience_type == "Experienced":
                if not company.strip():
                    invalid_fields.append("experience_company")
                if not job_role.strip():
                    invalid_fields.append("experience_role")
                if years is None:
                    invalid_fields.append("experience_years_input")

            if invalid_fields:
                st.session_state.profile_invalid_fields = invalid_fields
                st.rerun()

            profile.update({
                "first_name": first_name.strip(), "last_name": last_name.strip(),
                "email": email, "phone": phone.strip(), "date_of_birth": dob,
                "gender": gender, "city": city.strip(), "state": state.strip(),
                "address1": address1.strip(), "address2": address2.strip(),
                "pincode": pincode.strip(), "country": country.strip(),
                "skills": skills.strip(), "experience_type": experience_type,
                "company": company.strip(), "job_role": job_role.strip(),
                "years_experience": years, "expected_salary": expected_salary.strip(),
                "previous_salary": previous_salary.strip(),
            })
            st.session_state.profile_data = profile
            st.session_state.profile_invalid_fields = []
            st.success("Your profile has been saved in this demo session.")
    with cancel_col:
        st.button("Cancel", width="stretch", key="cancel_candidate_profile", on_click=_cancel_profile_edit)
