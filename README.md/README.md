# 📄 Resume Analyzer Bot

An interactive AI-based resume analyzer built using **Streamlit**, **spaCy**, and **pdfplumber**.

🎯 It extracts skills from your resume PDF, compares them with selected job roles (Full-Time or Internship), and provides:
- A resume **match score**
- **Matched vs. missing skills**
- A **PDF report**
- A **word cloud** of found keywords
- Optional: Upload a Job Description to compare with your resume

---

## 🧠 Features
- ✅ Internship vs. Full-Time skill evaluation
- ✅ 20+ roles with expected skillsets
- ✅ JD PDF upload + keyword matching
- ✅ Resume Score and improvement suggestions
- ✅ Word cloud of detected skills
- ✅ Downloadable PDF feedback report

---

## 🚀 How to Run

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Launch the app
streamlit run app.py
