import os

import streamlit as st
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_text_splitters import CharacterTextSplitter


# ==================================================
# PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="Tatyana Sysak | Innovation & Operations",
    page_icon="💼",
    layout="wide"
)


# ==================================================
# ENVIRONMENT
# ==================================================

load_dotenv()

API_KEY = os.getenv("OPENAI_API_KEY")


# ==================================================
# LOAD CV + CAREER INFORMATION & SETUP AI
# ==================================================

@st.cache_resource
def initialize_ai_brain():

    documents = []

    # --------------------------------------------------
    # Load CV
    # --------------------------------------------------

    cv_path = "Tatyana_Sysak_CV.pdf"

    if os.path.exists(cv_path):

        try:
            loader = PyPDFLoader(cv_path)
            cv_documents = loader.load()

            for doc in cv_documents:
                doc.metadata["source"] = "CV"
                documents.append(doc)

        except Exception as e:
            st.warning(f"Could not load CV: {e}")

    else:
        st.warning(
            f"{cv_path} was not found."
        )


    # --------------------------------------------------
    # Load Career Information
    # --------------------------------------------------

    career_path = "career information.pdf"

    if os.path.exists(career_path):

        try:
            loader = PyPDFLoader(career_path)
            career_documents = loader.load()

            for doc in career_documents:
                doc.metadata["source"] = "Career Information"
                documents.append(doc)

        except Exception as e:
            st.warning(
                f"Could not load Career Information: {e}"
            )

    else:
        st.warning(
            f"{career_path} was not found."
        )


    # --------------------------------------------------
    # Check documents
    # --------------------------------------------------

    if not documents:
        return None


    # --------------------------------------------------
    # Split documents into searchable chunks
    # --------------------------------------------------

    text_splitter = CharacterTextSplitter(
        chunk_size=700,
        chunk_overlap=100
    )

    chunks = text_splitter.split_documents(documents)


    # --------------------------------------------------
    # Check API key
    # --------------------------------------------------

    if not API_KEY:
        return None


    # --------------------------------------------------
    # Create embeddings
    # --------------------------------------------------

    embeddings = OpenAIEmbeddings(
        api_key=API_KEY
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )


    # --------------------------------------------------
    # Create AI model
    # --------------------------------------------------

    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.1,
        api_key=API_KEY
    )


    # --------------------------------------------------
    # Career assistant instructions
    # --------------------------------------------------

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """
You are Tatyana Sysak's AI career assistant.

Your job is to answer recruiters' questions as if
Tatyana herself is answering them.

The knowledge base contains two sources:

1. Tatyana's CV
2. Tatyana's Career Information document

Use BOTH sources when answering questions.

==================================================
FIRST-PERSON RULE
==================================================

ALWAYS answer in FIRST PERSON.

Use language such as:

"I"
"me"
"my"
"I've"
"I worked"
"I led"
"I coordinated"
"I supported"
"I have experience"
"I was responsible for"

NEVER describe Tatyana in the third person.

DO NOT say:

"Tatyana has experience..."
"Tatyana worked..."
"She has experience..."
"She worked..."
"Her responsibilities included..."

Instead say:

"I have experience..."
"I worked..."
"I coordinated..."
"My responsibilities included..."

The recruiter should feel like they are speaking
directly with Tatyana.

==================================================
ACCURACY RULES
==================================================

1. ONLY use information contained in the CV or
Career Information document.

2. Do not invent information.

3. Do not guess.

4. Do not make assumptions.

5. Do not create employers, job titles, dates,
responsibilities, achievements, skills, degrees,
projects or technologies that are not supported
by the documents.

6. Never exaggerate Tatyana's seniority or level
of responsibility.

7. If something is described as "supported",
"contributed to", or "coordinated", do not change
it to "managed", "owned", or "led" unless the
documents explicitly support that wording.

==================================================
USING BOTH DOCUMENTS
==================================================

Use the CV for factual career information such as:

- employers
- job titles
- dates
- education
- skills
- concise responsibilities

Use the Career Information document for richer
context such as:

- detailed responsibilities
- projects
- examples
- achievements
- challenges
- learning experiences
- cross-functional work
- explanations of what I actually did

When both documents contain information about
the same experience, combine them naturally.

Do not repeat the same information unnecessarily.

==================================================
ANSWER STYLE
==================================================

Answer the specific question being asked.

Do not simply list everything you know about me.

Keep answers:

- natural
- conversational
- professional
- concise
- specific
- recruiter-friendly

The answer should sound like something I would
actually say during an interview.

Do not sound like you are reading my CV.

When useful, give a concrete example from my
experience.

For example, instead of:

"I have project management experience."

Prefer:

"I've coordinated several cross-functional projects,
working with different teams to keep initiatives
moving and aligned."

==================================================
RELEVANCE
==================================================

Focus on the experience most relevant to the question.

For example:

If asked about project management:
focus on project coordination, cross-functional
projects, planning and execution.

If asked about operations:
focus on process improvement, operational efficiency,
coordination, reporting and digital tools.

If asked about knowledge management:
focus on knowledge-management projects, information
organization, portals, materials and search solutions.

If asked about leadership:
focus only on leadership or coordination experience
that is actually supported by the documents.

If asked about AI or automation:
focus on documented AI, automation, digital tools
and technology-related experience.

==================================================
WHEN INFORMATION IS MISSING
==================================================

If the information needed to answer the question
is not supported by either document, do not guess,
invent, or make assumptions.

Instead, ALWAYS respond with exactly:

"Looks like this one is beyond your credits 😄. Book a direct interview with me here and I’ll tell you all about it."

==================================================
ANSWER ENDING
==================================================

If you have enough information to answer the question,
ALWAYS end the answer with exactly:

"If you'd like to learn more about my experience or book an interview, you can do so here."


==================================================
KNOWLEDGE BASE
==================================================

{context}
"""
            ),
            (
                "human",
                "{question}"
            )
        ]
    )


    return {
        "vectorstore": vectorstore,
        "llm": llm,
        "prompt": prompt
    }


# Initialize AI
ai_brain = initialize_ai_brain()


# ==================================================
# DESIGN
# ==================================================

st.markdown(
    """
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
        color: #222;
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

    .skill {
        display: inline-block;
        padding: 0.5rem 0.9rem;
        margin: 0.3rem;
        border-radius: 20px;
        border: 1px solid #cccccc;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ==================================================
# ASK TATYANA
# ==================================================

st.markdown(
    """
    <div class="ask-container">
        <div class="ask-title">💬 Ask Tatyana</div>
        <div class="ask-subtitle">
            Ask me anything about my experience, projects, skills or career.
            Powered by AI.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)


with st.form(key="chat_form"):

    question = st.text_input(
        "Question",
        placeholder="What would you like to know about Tatyana?",
        label_visibility="collapsed"
    )

    submit_button = st.form_submit_button("Ask →")


if submit_button and question:

    if not API_KEY:

        st.error(
            "OpenAI API key not found. Please check your .env file."
        )

    elif not ai_brain:

        st.error(
            "The career knowledge base could not be initialized."
        )

    else:

        with st.spinner("Tatyana's AI is thinking..."):

            try:

                vectorstore = ai_brain["vectorstore"]
                llm = ai_brain["llm"]
                prompt = ai_brain["prompt"]


                # --------------------------------------------------
                # Find relevant information from BOTH documents
                # --------------------------------------------------

                retrieved_docs = vectorstore.similarity_search(
                    question,
                    k=6
                )


                # --------------------------------------------------
                # Combine retrieved information
                # --------------------------------------------------

                context_parts = []

                for doc in retrieved_docs:

                    source = doc.metadata.get(
                        "source",
                        "Career Information"
                    )

                    context_parts.append(
                        f"[Source: {source}]\n"
                        f"{doc.page_content}"
                    )


                context = "\n\n".join(
                    context_parts
                )


                # --------------------------------------------------
                # Build AI prompt
                # --------------------------------------------------

                messages = prompt.format_messages(
                    context=context,
                    question=question
                )


                # --------------------------------------------------
                # Ask AI
                # --------------------------------------------------

                response = llm.invoke(messages)

                answer = response.content


                # --------------------------------------------------
                # Display answer
                # --------------------------------------------------

                st.markdown(
                    '<div class="answer-box">',
                    unsafe_allow_html=True
                )

                st.markdown(
                    "**Tatyana's answer**"
                )

                st.write(answer)

                st.markdown(
                    '</div>',
                    unsafe_allow_html=True
                )


            except Exception as e:

                st.error(
                    f"An error occurred: {e}"
                )


st.divider()


# ==================================================
# HERO
# ==================================================

col1, col2 = st.columns([1, 2])


with col1:

    if os.path.exists("profile.jpeg"):

        st.image(
            "profile.jpeg",
            width=220
        )

    else:

        st.info(
            "Profile image not found."
        )


with col2:

    st.markdown(
        '<div class="hero-title">Tatyana Sysak</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="hero-subtitle">'
        'Innovation & Operations | AI & Automation'
        '</div>',
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

        if os.path.exists("Tatyana_Sysak_CV.pdf"):

            with open(
                "Tatyana_Sysak_CV.pdf",
                "rb"
            ) as file:

                st.download_button(
                    "📄 Download CV",
                    data=file.read(),
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
        "September 2022 – July 2026"
    ),

    (
        "University of Twente",
        "Master of Business Administration — Innovation & Strategy",
        "August 2023 – July 2024"
    ),

    (
        "Anglia Ruskin University",
        "BSc (Hons) Business Management — Tourism & Events Management",
        "September 2018 – August 2021"
    ),

    (
        "Munich University of Applied Sciences",
        "Erasmus+ Semester",
        "2020"
    )

]


for university, degree, dates in education:

    st.markdown(
        f"### {university}"
    )

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


skills_html = "".join(
    [
        f'<span class="skill">{skill}</span>'
        for skill in skills
    ]
)


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