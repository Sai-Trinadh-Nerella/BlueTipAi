import streamlit as st
from datetime import datetime
import re

def render_candidate_profile():
    # Initialize validation state flag
    if "validation_failed" not in st.session_state:
        st.session_state.validation_failed = False
    if "missing_fields" not in st.session_state:
        st.session_state.missing_fields = []

    # Helper Functions & Sanitization
    def sanitize_pincode():
        if "pincode" in st.session_state:
            st.session_state["pincode"] = "".join(
                char for char in st.session_state["pincode"] if char in "0123456789"
            )[:6]

    def valid_email(value):
        return re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", (value or "").strip()) is not None

    def valid_person_name(value):
        val = (value or "").strip()
        return bool(val) and any(char.isalpha() for char in val) and all(
            char.isalpha() or char in " '-." for char in val
        )

    def save_data_and_reset(new_data):
        st.session_state.education_history.append(new_data)
        st.session_state.edu_level = None
        st.rerun()

    # Dynamic Red Highlighting CSS for missing/invalid fields
    if st.session_state.validation_failed:
        error_css = "<style>"
        for key in st.session_state.missing_fields:
            error_css += f"""
            div[data-aria-label="{key}"] input,
            div[data-testid="stTextInput"]:has(input[aria-label*="{key}"]) input,
            div[data-testid="stSelectbox"]:has(div[aria-label*="{key}"]) > div,
            div[data-testid="stDateInput"]:has(input[aria-label*="{key}"]) input {{
                border: 2px solid #FF4B4B !important;
                border-radius: 8px !important;
                background-color: rgba(255, 75, 75, 0.05) !important;
            }}
            """
        error_css += "</style>"
        st.markdown(error_css, unsafe_allow_html=True)

    st.caption("* Required field. Fields marked Optional may be left blank.")

    # ==========================================
    # 1. PERSONAL INFORMATION & RESUME UPLOAD
    # ==========================================
    st.subheader("Personal Information")

    col1, col2 = st.columns(2)
    with col1:
        First_name = st.text_input("First Name *", placeholder="Enter first name", key="input_first_name")
        Email = st.text_input("Email ID *", value=st.session_state.get("candidate_email", ""), key="input_email")
        dob = st.date_input("Date of Birth *", value=None, key="input_dob")

    with col2:
        Last_name = st.text_input("Last Name *", placeholder="Enter last name", key="input_last_name")
        Phone = st.text_input("Phone number *", placeholder="10-digit mobile number", key="input_phone")
        gender = st.selectbox(
            "Select Gender *",
            ["Male", "Female", "Other"],
            index=None,
            placeholder="Select Gender",
            key="input_gender"
        )

    resume_file = st.file_uploader(
        "Upload Resume / CV (Optional, PDF or DOCX, Max 5MB)", 
        type=["pdf", "docx"], 
        key="resume_upload"
    )

    st.divider()

    # ==========================================
    # 2. ADDRESS DETAILS
    # ==========================================
    st.subheader("Address Details")

    address1 = st.text_input("Address Line 1 *", placeholder="House no., Street, Area", key="input_address1")
    address2 = st.text_input("Address Line 2 (Optional)", placeholder="Apartment, Suite, Unit, etc.", key="input_address2")

    col3, col4 = st.columns(2)
    with col3:
        city = st.text_input("City / Town *", placeholder="Enter city", key="input_city")
        pincode = st.text_input(
            "Postal / Pin Code *",
            max_chars=6,
            key="pincode",
            on_change=sanitize_pincode,
            placeholder="6-digit pin code"
        )

    with col4:
        state = st.text_input("State *", placeholder="Enter state", key="input_state")
        country = st.text_input("Country *", placeholder="Enter country", key="input_country")

    st.divider()

    # ==========================================
    # 3. EDUCATIONAL DETAILS
    # ==========================================
    st.subheader("Educational Details")

    if "education_history" not in st.session_state:
        st.session_state.education_history = []

    if "edu_level" not in st.session_state:
        st.session_state.edu_level = None

    edu_options = ["", "High School", "Intermediate", "Diploma", "Bachelor's Degree", "Master's Degree", "Ph.D."]

    if st.session_state.education_history:
        st.write("### Saved Qualifications")
        for idx, item in enumerate(st.session_state.education_history):
            with st.expander(f"📌 {item['Level']} Details", expanded=False):
                col_e1, col_e2 = st.columns(2)
                with col_e1:
                    st.write(f"**Board / Stream / Degree:** {item['Board/Degree/Stream']}")
                    st.write(f"**Institution / School:** {item['Institution']}")
                with col_e2:
                    st.write(f"**Score / CGPA:** {item['Score'] if item['Score'] is not None else '-'}")
                    st.write(f"**Passing Year:** {item['Passing/Completion Year'] if item['Passing/Completion Year'] is not None else '-'}")
                if item.get("Joining Year"):
                    st.write(f"**Joining Year:** {item['Joining Year']}")
                st.write(f"**Status:** {item['Status']}")

        if st.button("Clear All and Start Over", key="clear_edu"):
            st.session_state.education_history = []
            st.session_state.edu_level = None
            st.rerun()

    st.write("Please fill in your academic background below.")

    current_year = datetime.now().year
    years_range = list(range(current_year - 20, current_year + 6))

    current_index = 0
    if st.session_state.edu_level in edu_options:
        current_index = edu_options.index(st.session_state.edu_level)

    selected_selection = st.selectbox(
        "Select Education Level to Add *",
        edu_options,
        index=current_index,
        format_func=lambda x: "Choose a level..." if x == "" else x,
        key="select_edu_dropdown"
    )

    if selected_selection == "":
        st.session_state.edu_level = None
    else:
        st.session_state.edu_level = selected_selection

    edu_level = st.session_state.edu_level

    # --- High School Form ---
    if edu_level == "High School":
        st.subheader("High School Details")
        col_hs1, col_hs2 = st.columns(2)
        with col_hs1:
            board = st.selectbox("Education Board *", ["CBSE", "ICSE", "State Board", "IB", "IGCSE", "Other"], index=None, placeholder="Select an education board", key="hs_board")
            school_name = st.text_input("School Name *", key="hs_school")
        with col_hs2:
            gpa = st.number_input("Marks / CGPA / Percentage *", min_value=0.0, max_value=100.0, value=None, step=0.01, format="%.2f", key="hs_gpa")
            passing_year = st.selectbox("Year of Passing *", years_range, index=None, placeholder="Select a year", key="hs_year")

        uploaded_file = st.file_uploader("Upload Marksheet (Optional, PDF, Max 5MB)", type=["pdf"], key="hs_file")

        if st.button("Save High School Details", key="btn_save_hs"):
            if not school_name.strip() or board is None or gpa is None or passing_year is None:
                st.warning("Please fill required fields for High School.")
            else:
                save_data_and_reset({
                    "Level": edu_level,
                    "Institution": school_name,
                    "Board/Degree/Stream": board,
                    "Score": gpa,
                    "Joining Year": None,
                    "Passing/Completion Year": passing_year,
                    "Status": "Completed"
                })

    # --- Intermediate Form ---
    elif edu_level == "Intermediate":
        st.subheader("Intermediate / Higher Secondary Details")
        col_in1, col_in2 = st.columns(2)
        with col_in1:
            inter_board = st.selectbox("Board of Education *", ["State Board", "CBSE", "ISC", "NIOS", "Other"], index=None, placeholder="Select a board", key="inter_board")
            college_name = st.text_input("Junior College / School Name *", key="inter_college")
            stream = st.selectbox("Stream / Group *", ["MPC (Maths, Physics, Chemistry)", "BIPC (Biology, Physics, Chemistry)", "CEC (Commerce, Economics, Civics)", "HEC (History, Economics, Civics)", "MEC (Maths, Economics, Commerce)", "Other"], index=None, placeholder="Select a stream", key="inter_stream")
        with col_in2:
            gpa = st.number_input("Marks / CGPA / Percentage *", min_value=0.0, max_value=100.0, value=None, step=0.01, format="%.2f", key="inter_gpa")
            joining_year = st.selectbox("Year of Joining *", years_range, index=None, placeholder="Select a year", key="inter_join")
            passing_year = st.selectbox("Year of Passing *", years_range, index=None, placeholder="Select a year", key="inter_pass")

        if joining_year is not None and passing_year is not None and passing_year < joining_year:
            st.error("Year of Passing cannot be earlier than Year of Joining.")

        uploaded_file = st.file_uploader("Upload Intermediate Certificate (Optional, PDF, Max 5MB)", type=["pdf"], key="inter_file")

        if st.button("Save Intermediate Details", key="btn_save_inter"):
            if not college_name.strip() or inter_board is None or stream is None or gpa is None or joining_year is None or passing_year is None:
                st.warning("Please fill required fields for Intermediate.")
            elif passing_year < joining_year:
                st.error("Please fix timeline errors before saving.")
            else:
                save_data_and_reset({
                    "Level": edu_level,
                    "Institution": college_name,
                    "Board/Degree/Stream": f"{inter_board} - {stream}",
                    "Score": gpa,
                    "Joining Year": joining_year,
                    "Passing/Completion Year": passing_year,
                    "Status": "Completed"
                })

    # --- Diploma Form ---
    elif edu_level == "Diploma":
        st.subheader("Diploma Details")
        col_dp1, col_dp2 = st.columns(2)
        with col_dp1:
            diploma_field = st.text_input("Field of Diploma *", key="dip_field")
            institute_name = st.text_input("Institute/Polytechnic Name *", key="dip_inst")
        with col_dp2:
            gpa = st.number_input("CGPA / Percentage *", min_value=0.0, max_value=100.0, value=None, step=0.01, format="%.2f", key="dip_gpa")
            joining_year = st.selectbox("Year of Joining *", years_range, index=None, placeholder="Select a year", key="dip_join")
            passing_year = st.selectbox("Year of Passing *", years_range, index=None, placeholder="Select a year", key="dip_pass")

        if joining_year is not None and passing_year is not None and passing_year < joining_year:
            st.error("Year of Passing cannot be earlier than Year of Joining.")

        uploaded_file = st.file_uploader("Upload Diploma Certificate (Optional, PDF, Max 5MB)", type=["pdf"], key="dip_file")

        if st.button("Save Diploma Details", key="btn_save_dip"):
            if not institute_name.strip() or not diploma_field.strip() or gpa is None or joining_year is None or passing_year is None:
                st.warning("Please fill required fields for Diploma.")
            elif passing_year < joining_year:
                st.error("Please fix timeline errors before saving.")
            else:
                save_data_and_reset({
                    "Level": edu_level,
                    "Institution": institute_name,
                    "Board/Degree/Stream": diploma_field,
                    "Score": gpa,
                    "Joining Year": joining_year,
                    "Passing/Completion Year": passing_year,
                    "Status": "Completed"
                })

    # --- Bachelor's Degree Form ---
    elif edu_level == "Bachelor's Degree":
        st.subheader("Bachelor's Degree Details")
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            bachelor_degree = st.selectbox("Degree Type *", ["B.Tech", "B.E.", "B.Sc", "B.Com", "B.A.", "B.B.A.", "Other"], index=None, placeholder="Select a degree type", key="bach_type")
            college_name = st.text_input("College/University Name *", key="bach_college")
        with col_b2:
            stream = st.selectbox("Stream / Discipline *", ["Computer Science & Engineering (CSE)", "Information Technology (IT)", "Electronics & Communication (ECE)", "Mechanical Engineering (ME)", "Civil Engineering (CE)", "Electrical Engineering (EEE)", "Other"], index=None, placeholder="Select a stream", key="bach_stream")
            gpa = st.number_input("CGPA / Percentage *", min_value=0.0, max_value=100.0, value=None, step=0.01, format="%.2f", key="bach_gpa")

        col_b3, col_b4 = st.columns(2)
        with col_b3:
            joining_year = st.selectbox("Year of Joining *", years_range, index=None, placeholder="Select a year", key="bach_join")
        with col_b4:
            passing_year = st.selectbox("Year of Passing / Expected *", years_range, index=None, placeholder="Select a year", key="bach_pass")

        if joining_year is not None and passing_year is not None and passing_year < joining_year:
            st.error("Year of Passing cannot be earlier than Year of Joining.")

        uploaded_file = st.file_uploader("Upload Degree Certificate (Optional, PDF, Max 5MB)", type=["pdf"], key="bach_file")

        if st.button("Save Bachelor's Details", key="btn_save_bach"):
            if not college_name.strip() or bachelor_degree is None or stream is None or gpa is None or joining_year is None or passing_year is None:
                st.warning("Please fill required fields for Bachelor's Degree.")
            elif passing_year < joining_year:
                st.error("Please fix timeline errors before saving.")
            else:
                save_data_and_reset({
                    "Level": edu_level,
                    "Institution": college_name,
                    "Board/Degree/Stream": f"{bachelor_degree} ({stream})",
                    "Score": gpa,
                    "Joining Year": joining_year,
                    "Passing/Completion Year": passing_year,
                    "Status": "Completed"
                })

    # --- Master's Degree Form ---
    elif edu_level == "Master's Degree":
        st.subheader("Master's Degree Details")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            masters_degree = st.selectbox("Degree Type *", ["M.Tech", "M.E.", "M.Sc", "M.Com", "M.A.", "MBA", "MCA", "Other"], index=None, placeholder="Select a degree type", key="mast_type")
            university_name = st.text_input("University/Institute Name *", key="mast_uni")
        with col_m2:
            specialization = st.text_input("Specialization / Major *", key="mast_spec")
            gpa = st.number_input("CGPA / Percentage *", min_value=0.0, max_value=100.0, value=None, step=0.01, format="%.2f", key="mast_gpa")

        col_m3, col_m4 = st.columns(2)
        with col_m3:
            joining_year = st.selectbox("Year of Joining *", years_range, index=None, placeholder="Select a year", key="mast_join")
        with col_m4:
            passing_year = st.selectbox("Year of Passing / Expected *", years_range, index=None, placeholder="Select a year", key="mast_pass")

        if joining_year is not None and passing_year is not None and passing_year < joining_year:
            st.error("Year of Passing cannot be earlier than Year of Joining.")

        uploaded_file = st.file_uploader("Upload Master's Certificate (Optional, PDF, Max 5MB)", type=["pdf"], key="mast_file")

        if st.button("Save Master's Details", key="btn_save_mast"):
            if not university_name.strip() or not specialization.strip() or masters_degree is None or gpa is None or joining_year is None or passing_year is None:
                st.warning("Please fill required fields for Master's Degree.")
            elif passing_year < joining_year:
                st.error("Please fix timeline errors before saving.")
            else:
                save_data_and_reset({
                    "Level": edu_level,
                    "Institution": university_name,
                    "Board/Degree/Stream": f"{masters_degree} ({specialization})",
                    "Score": gpa,
                    "Joining Year": joining_year,
                    "Passing/Completion Year": passing_year,
                    "Status": "Completed"
                })

    # --- Ph.D. Form ---
    elif edu_level == "Ph.D.":
        st.subheader("Ph.D. Research Details")
        col_p1, col_p2 = st.columns(2)
        with col_p1:
            phd_institute = st.text_input("University / Institute Name *", key="phd_inst")
            research_topic = st.text_input("Research Topic / Thesis Title *", key="phd_topic")
        with col_p2:
            guide_name = st.text_input("Research Guide (Optional)", key="phd_guide")
            phd_status = st.selectbox("Status *", ["Ongoing", "Submitted", "Awarded"], index=None, placeholder="Select a status", key="phd_status")

        col_p3, col_p4 = st.columns(2)
        with col_p3:
            joining_year = st.selectbox("Year of Enrollment *", years_range, index=None, placeholder="Select a year", key="phd_join")
        with col_p4:
            completion_year = st.selectbox("Year of Completion / Expected *", years_range, index=None, placeholder="Select a year", key="phd_comp")

        if joining_year is not None and completion_year is not None and completion_year < joining_year:
            st.error("Year of Completion cannot be earlier than Year of Enrollment.")

        uploaded_file = st.file_uploader("Upload Thesis Synopsis (Optional, PDF, Max 5MB)", type=["pdf"], key="phd_file")

        if st.button("Save Ph.D. Details", key="btn_save_phd"):
            if not phd_institute.strip() or not research_topic.strip() or joining_year is None or completion_year is None or phd_status is None:
                st.warning("Please fill required fields for Ph.D.")
            elif completion_year < joining_year:
                st.error("Please fix timeline errors before saving.")
            else:
                save_data_and_reset({
                    "Level": edu_level,
                    "Institution": phd_institute,
                    "Board/Degree/Stream": research_topic,
                    "Score": None,
                    "Joining Year": joining_year,
                    "Passing/Completion Year": completion_year,
                    "Status": phd_status
                })

    st.divider()

    # ==========================================
    # 4. PROFESSIONAL EXPERIENCE
    # ==========================================
    st.subheader("Professional Experience")

    experience_type = st.selectbox(
        "Are you a Fresher or Experienced? *",
        ["Fresher", "Experienced"],
        index=None,
        placeholder="Select experience level",
        key="exp_type_selectbox"
    )

    previous_company = ""
    Job_Role = ""
    Years_of_Experience = None
    Technical_skills = ""
    Previous_Salary = None
    Expected_Salary = None

    if experience_type == "Experienced":
        previous_company = st.text_input("Previous Company *", key="exp_company")
        Job_Role = st.text_input("Job Role *", key="exp_role")
        Years_of_Experience = st.number_input(
            "Years of Experience *", min_value=0, max_value=50, value=None, step=1, key="exp_years"
        )
        Technical_skills = st.text_area("Technical Skills *", key="exp_tech_exp")
        Previous_Salary = st.number_input(
            "Previous Salary (per annum) *", min_value=0, value=None, step=1000, key="exp_prev_sal"
        )
        Expected_Salary = st.number_input(
            "Expected Salary (per annum) *", min_value=0, value=None, step=1000, key="exp_exp_sal"
        )
    elif experience_type == "Fresher":
        Technical_skills = st.text_area("Technical Skills *", key="exp_tech_fresh")
        Expected_Salary = st.number_input(
            "Expected Salary (per annum) *", min_value=0, value=None, step=1000, key="exp_fresh_sal"
        )

    st.divider()

    # ==========================================
    # 5. PROJECTS DONE
    # ==========================================
    if "projects_history" not in st.session_state:
        st.session_state.projects_history = []

    if experience_type is not None:
        st.subheader("Projects Done (Optional)")
        st.caption("If you add a project, its title, description, and technologies are required.")

        if st.session_state.projects_history:
            st.write("### Saved Projects")
            for idx, proj in enumerate(st.session_state.projects_history):
                with st.expander(f"🚀 {proj['Project Title']}", expanded=False):
                    st.write(f"**Description:** {proj['Description']}")
                    st.write(f"**Technologies Used:** {proj['Technologies']}")
                    st.write(f"**Project Link / GitHub:** {proj['Link'] if proj['Link'] else '-'}")

        proj_title = st.text_input("Project Title *", key="input_proj_title")
        proj_desc = st.text_area("Project Description *", key="input_proj_desc")
        proj_tech = st.text_input("Technologies Used *", key="input_proj_tech")
        proj_link = st.text_input("Project Link / GitHub URL (Optional)", key="input_proj_link")

        if st.button("Save Project", key="btn_save_project"):
            if not proj_title.strip() or not proj_desc.strip() or not proj_tech.strip():
                st.warning("Please fill required fields for Project.")
            elif proj_link.strip() and not re.fullmatch(r"https?://\S+", proj_link.strip()):
                st.warning("Enter a valid URL starting with http:// or https://.")
            else:
                st.session_state.projects_history.append({
                    "Project Title": proj_title,
                    "Description": proj_desc,
                    "Technologies": proj_tech,
                    "Link": proj_link
                })
                st.success("Project added successfully!")
                st.rerun()

    st.divider()

    # ==========================================
    # 6. PROFILE PHOTO & FINAL SAVE CONTROLS
    # ==========================================
    st.subheader("Profile Photo")
    profile_photo = st.file_uploader(
        "Upload profile photo (Optional, Max 5MB)", type=["jpg", "jpeg", "png"], key="profile_photo_upload"
    )

    st.divider()

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Save Profile Details", type="primary", use_container_width=True, key="btn_final_save"):
            missing = []
            
            if not valid_person_name(First_name):
                missing.append("First Name *")
            if not valid_person_name(Last_name):
                missing.append("Last Name *")
            if not valid_email(Email):
                missing.append("Email ID *")
            if len(Phone or "") != 10 or not (Phone or "").isdigit():
                missing.append("Phone number *")
            if dob is None:
                missing.append("Date of Birth *")
            if gender is None:
                missing.append("Select Gender *")
            if not (address1 or "").strip():
                missing.append("Address Line 1 *")
            if not (city or "").strip():
                missing.append("City / Town *")
            if not (state or "").strip():
                missing.append("State *")
            if not (country or "").strip():
                missing.append("Country *")
            if len(st.session_state.get("pincode", "")) != 6:
                missing.append("Postal / Pin Code *")
            if not st.session_state.education_history:
                missing.append("Select Education Level to Add *")
            if experience_type is None:
                missing.append("Are you a Fresher or Experienced? *")

            if missing:
                st.session_state.validation_failed = True
                st.session_state.missing_fields = missing
                st.warning("⚠️ Please fill required fields")
                st.rerun()
            else:
                st.session_state.validation_failed = False
                st.session_state.missing_fields = []
                st.success("Candidate details saved successfully!")

    with col_btn2:
        if st.button("Cancel", use_container_width=True, key="btn_final_cancel"):
            st.session_state.validation_failed = False
            st.session_state.missing_fields = []
            st.info("Edit cancelled.")