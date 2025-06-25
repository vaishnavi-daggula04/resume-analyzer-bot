import streamlit as st
import spacy
import pdfplumber
import re
from fpdf import FPDF
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import spacy.cli
spacy.cli.download("en_core_web_sm")


# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Predefined skills
SKILL_KEYWORDS = [
    'python', 'machine learning', 'data analysis', 'deep learning', 'nlp',
    'sql', 'powerbi', 'excel', 'tableau', 'pandas', 'numpy', 'tensorflow',
    'keras', 'pytorch', 'communication', 'teamwork', 'leadership',
    'hadoop', 'spark', 'aws', 'django', 'flask', 'html', 'css', 'javascript', 'react'
]

ROLE_SKILLS = {
    "Full-Time": {
        "data scientist": ['python', 'machine learning', 'pandas', 'numpy', 'sql', 'matplotlib', 'seaborn'],
        "data analyst": ['excel', 'powerbi', 'tableau', 'sql', 'data analysis', 'pandas'],
        "ml engineer": ['python', 'tensorflow', 'keras', 'pytorch', 'deep learning', 'mlops'],
        "data engineer": ['python', 'sql', 'hadoop', 'spark', 'aws', 'etl', 'airflow'],
        "backend developer": ['python', 'django', 'flask', 'sql', 'docker', 'rest api'],
        "frontend developer": ['html', 'css', 'javascript', 'react', 'typescript'],
        "full stack developer": ['html', 'css', 'javascript', 'react', 'python', 'django', 'sql'],
        "business analyst": ['excel', 'sql', 'data visualization', 'tableau', 'powerbi', 'presentation'],
        "ai researcher": ['python', 'pytorch', 'tensorflow', 'research', 'deep learning', 'nlp'],
        "cloud engineer": ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'linux', 'terraform'],
        "devops engineer": ['jenkins', 'docker', 'kubernetes', 'linux', 'ci/cd', 'aws', 'git'],
        "cybersecurity analyst": ['network security', 'firewalls', 'siem', 'linux', 'python'],
        "mobile developer": ['android', 'kotlin', 'java', 'flutter', 'react native'],
        "ui/ux designer": ['figma', 'adobe xd', 'wireframes', 'prototyping', 'user research'],
        "product manager": ['roadmap', 'market research', 'agile', 'user stories', 'scrum', 'analytics'],
        "technical writer": ['documentation', 'api writing', 'markdown', 'github', 'confluence'],
        "qa engineer": ['selenium', 'test cases', 'automation', 'pytest', 'manual testing'],
        "blockchain developer": ['solidity', 'web3', 'ethereum', 'smart contracts', 'metamask'],
        "game developer": ['unity', 'c#', '3d modeling', 'unreal engine', 'game physics'],
        "graphic designer": ['photoshop', 'illustrator', 'creativity', 'branding', 'typography']
    },
    "Internship": {
        "data scientist": ['python', 'machine learning', 'pandas', 'numpy'],
        "data analyst": ['excel', 'powerbi', 'tableau', 'data analysis'],
        "ml engineer": ['python', 'tensorflow', 'keras'],
        "frontend developer": ['html', 'css', 'javascript'],
        "backend developer": ['python', 'django', 'sql'],
        "ui/ux designer": ['figma', 'wireframes', 'prototyping'],
        "qa engineer": ['manual testing', 'selenium', 'bug reporting']
    }
}

def extract_text_from_pdf(uploaded_file):
    text = ""
    with pdfplumber.open(uploaded_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_skills(text):
    doc = nlp(text.lower())
    skills = set()
    for token in doc:
        if token.text in SKILL_KEYWORDS:
            skills.add(token.text)
    return list(skills)

def score_resume(skills, selected_role, job_type):
    expected_skills = ROLE_SKILLS[job_type].get(selected_role.lower(), [])
    matched = [s for s in skills if s in expected_skills]
    score = round((len(matched) / len(expected_skills)) * 100, 2) if expected_skills else 0
    if job_type == "Internship":
        score = min(score + 15, 100)  # Give internship applicants a slight boost
    return matched, score, expected_skills

def generate_pdf_report(matched, missing, score, selected_role):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resume Analysis Report", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"Target Role: {selected_role}\n\nMatched Skills: {', '.join(matched)}\n\nMissing Skills: {', '.join(missing)}\n\nScore: {score}%")
    pdf_output = io.BytesIO()
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    pdf_output.write(pdf_bytes)
    pdf_output.seek(0)
    return pdf_output

def show_wordcloud(skills):
    wordcloud = WordCloud(width=600, height=400, background_color='white').generate(' '.join(skills))
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

# ---------------- Streamlit UI ---------------- #

st.set_page_config(page_title="Resume Analyzer Bot", layout="centered")
st.title("\U0001F4C4 Resume Analyzer Bot")
st.write("Upload your resume (PDF) and optionally a job description PDF to see how well it matches!")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf"])
job_type = st.radio("Select Type", ["Full-Time", "Internship"])
selected_role = st.selectbox("Select Target Job Role", ["Choose a role"] + list(ROLE_SKILLS[job_type].keys()))
job_description_file = st.file_uploader("Optional: Upload Job Description PDF", type=["pdf"])

if uploaded_file and selected_role != "Choose a role":
    resume_text = extract_text_from_pdf(uploaded_file)
    resume_skills = extract_skills(resume_text)
    matched_skills, score, expected = score_resume(resume_skills, selected_role, job_type)
    missing = set(expected) - set(matched_skills)

    st.subheader("✅ Skills Found in Resume")
    st.write(", ".join(resume_skills) if resume_skills else "No matching skills found.")

    st.subheader("🎯 Skills Matched for Role")
    st.write(", ".join(matched_skills) if matched_skills else "No matched skills for this role.")

    st.subheader("📊 Resume Score")
    st.progress(score / 100)
    st.success(f"Your resume matches {score}% of the expected skills for a {job_type.lower()} {selected_role} role.")

    st.subheader("📌 Suggestions")
    if job_type == "Internship":
        st.info("For internships, focus on showcasing your projects, certifications, and academic knowledge.")
    if missing:
        st.warning(f"Consider adding these skills: {', '.join(missing)}")
    else:
        st.success("Excellent! Your resume includes all key skills for this role.")

    if job_description_file:
        jd_text = extract_text_from_pdf(job_description_file)
        jd_skills = extract_skills(jd_text)
        jd_missing = set(jd_skills) - set(resume_skills)
        st.subheader("📝 Job Description Match")
        st.write(f"Found these keywords in JD not present in resume: {', '.join(jd_missing)}")

    with st.expander("🔍 View Extracted Resume Text"):
        st.write(resume_text)

    st.subheader("☁️ Skill Word Cloud")
    show_wordcloud(resume_skills)

    st.subheader("📥 Downloadable Resume Report")
    pdf_bytes = generate_pdf_report(matched_skills, missing, score, selected_role)
    st.download_button("📄 Download PDF Report", data=pdf_bytes, file_name="resume_report.pdf", mime="application/pdf")

elif uploaded_file:
    st.info("👉 Please select a job role to get resume feedback.")
