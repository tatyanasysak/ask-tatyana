import json
import streamlit as st

# ==================================================
# LOAD CAREER DATA
# ==================================================

with open("career.json", "r", encoding="utf-8") as file:
    career_data = json.load(file)


# ==================================================
# QUESTION MATCHING
# ==================================================

def find_answer(question):
    question = question.lower()

    if "siemens" in question:
        return career_data[1]["answer"]

    if "background" in question or "career" in question:
        return career_data[0]["answer"]

    if "project" in question or "ownership" in question:
        return career_data[2]["answer"]

    if "skills" in question or "strengths" in question:
        return career_data[3]["answer"]

    if "ai" in question or "automation" in question:
        return career_data[4]["answer"]

    return "I don't have an answer to that question yet."


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Tatyana Sysak | Innovation & Operations",
    page_icon="💼",
    layout="wide"
)


# ==================================================
# DESIGN
# ==================================================

st.markdown("""
<style>

.ask-container {
    padding: 1.5rem;
    border: 1px solid #dddddd;
    border-radius: 18px;
    margin-bottom: 1rem;
    background-color: white;
}

.ask-title {
    font-size: 1.6rem;
    font-weight: 700;
}

.ask-subtitle {
    font-size: 1rem;
    color: #666666;
}

.answer-box {
    padding: 1.2rem;
    border-radius: 14px;
    border: 1px solid #dddddd;
    margin-top: 1rem;
    background-color: #fafafa;
}

.hero-title {
    font-size: 3rem;
    font-weight: 700;
}

.hero-subtitle {
    font-size: 1.4rem;
    color: #555555;
    margin-bottom: 1rem;
}

.section-title {
    font-size: 2rem;
    font-weight: 650;
    margin-top: 2rem;
    margin-bottom: 1rem;
}

.education-card {
    padding: 1.2rem;
    border-radius: 14px;
    border: 1px solid #dddddd;
    margin-bottom: 1rem;
    background-color: white;
}

.education-school {
    font-size: 1.1rem;
    font-weight: 650;
}

.education-degree {
    margin-top: 0.4rem;
}

.education-date {
    color: #777777;
    font-size: 0.9rem;
    margin-top: 0.4rem;
}

.skill {
    display: inline-block;
    padding: 0.5rem 0.9rem;
    margin: 0.3rem;
    border-radius: 20px;
    border: 1px solid #cccccc;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# ASK TATYANA
# ==================================================

st.markdown("""
<div class="ask-container">

<div class="ask-title">
💬 Ask Tatyana
</div>

<div class="ask-subtitle">
Ask me anything about my experience, projects, skills or career.
</div>

</div>
""", unsafe_allow_html=True)


question = st.text_input(
    "Question",
    placeholder="What would you like to know about Tatyana?",
    label_visibility="collapsed"
)


if st.button("Ask →"):

    if question:

        answer = find_answer(question)

        st.markdown(
            '<div class="answer-box">',
            unsafe_allow_html=True
        )

        st.markdown("**Tatyana's answer**")

        st.write(answer)

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


st.divider()


# ==================================================
# HERO
# ==================================================

col1, col2 = st.columns([1, 2])


with col1:

    st.image(
    "profile.jpeg",
    width=220
)


with col2:

    st.markdown(
        '<div class="hero-title">Tatyana Sysak</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">Innovation & Operations | AI & Automation</div>',
        unsafe_allow_html=True
    )

    st.write(
        """
        Business and innovation professional with an interdisciplinary
        background in business, entrepreneurship, strategy and innovation.

        Interested in using technology, AI and automation to improve
        the way people and organisations work.
        """
    )

    col_email, col_cv = st.columns(2)

    with col_email:

        st.link_button(
            "✉️ Email me",
            "mailto:taatiana.sysak@gmail.com"
        )

    with col_cv:

        st.download_button(
    "📄 Download CV",
    data=open("Tatyana_Sysak_CV.pdf", "rb").read(),
    file_name="Tatyana_Sysak_CV.pdf",
    mime="application/pdf"
)


st.divider()


# ==================================================
# ABOUT
# ==================================================

st.markdown(
    '<div class="section-title">About me</div>',
    unsafe_allow_html=True
)

st.write(
    """
    I am an innovation and operations professional with an interdisciplinary
    background in business, entrepreneurship, strategy and innovation.

    Throughout my academic and professional experience, I have worked across
    project coordination, knowledge management, operations, research,
    marketing and digital tools.

    I am particularly interested in how AI and automation can be applied
    to solve practical problems and make organisations work more effectively.
    """
)


# ==================================================
# EDUCATION
# ==================================================

st.markdown(
    '<div class="section-title">Education</div>',
    unsafe_allow_html=True
)


education = [
    (
        "Technische Universität Berlin",
        "Master of Science — Innovation Management, Entrepreneurship & Sustainability (IMES)",
        "October 2022 – August 2026"
    ),
    (
        "University of Twente",
        "Master of Business Administration — Entrepreneurship & Strategy",
        "September 2023 – September 2024"
    ),
    (
        "Anglia Ruskin University",
        "BSc (Hons) Business Management, Tourism & Travel Services Management",
        "2018 – 2021"
    ),
    (
        "Munich University of Applied Sciences",
        "Erasmus+ Semester — Tourism Management & Business Administration",
        "2020"
    )
]


for university, degree, dates in education:

    st.markdown(f"### {university}")

    st.write(degree)

    st.caption(dates)

    st.divider()


# ==================================================
# SKILLS
# ==================================================

st.markdown(
    '<div class="section-title">Skills</div>',
    unsafe_allow_html=True
)


skills = [
    "Project Management",
    "Operations",
    "Innovation",
    "Business Strategy",
    "Stakeholder Management",
    "Knowledge Management",
    "Process Improvement",
    "Research & Analysis",
    "AI & Automation",
    "Power BI",
    "Monday.com",
    "Content & Marketing"
]


skills_html = ""

for skill in skills:

    skills_html += f'<span class="skill">{skill}</span>'


st.markdown(
    skills_html,
    unsafe_allow_html=True
)


# ==================================================
# FOOTER
# ==================================================

st.divider()

st.caption(
    "Built by Tatyana Sysak • Exploring AI, automation and digital tools"
)