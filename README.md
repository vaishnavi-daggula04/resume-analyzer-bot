# 📄 Resume Analyzer Bot

🚀 An AI-powered Resume Analyzer built using **Streamlit** and **spaCy**. Upload your resume in PDF format and get:

- ✅ Extracted skills (technical + soft)
- 🎯 Match with selected job roles
- 📊 Resume score with suggestions
- ☁️ Word cloud of identified skills
- 📥 Downloadable PDF report
- 📝 Optional JD (Job Description) matching

---

## 🚀 Live Demo
[🌐 Open Streamlit App](https://vaishnavi-daggula04-resume-analyzer-bot.streamlit.app)

## ⚙️ Getting Started (Run Locally)
Clone the repository:
bash
git clone https://github.com/vaishnavi-daggula04/resume-analyzer-bot.git
cd resume-analyzer-bot

---

## 🧠 Features

- Supports **Internship** and **Full-Time** roles
- Role-wise skill matching using `spaCy` NLP
- PDF parsing using `pdfplumber`
- Skill cloud visualization with `WordCloud`
- Custom PDF feedback report using `FPDF`

---

## 📁 Project Structure

resume-analyzer-bot/
│
├── app.py # Main Streamlit app
├── requirements.txt # Python dependencies
├── sample_resume.pdf # (Optional) Sample resume for testing
├── README.md # Project documentation
├── streamlit/ # Config or extra files
├── py # (Optional/Unclear — remove if not needed)
└── venv/ # Virtual environment (ignored via .gitignore)

## 🛠️ Getting Started (Run Locally)

1. **Clone the repo:**

git clone https://github.com/vaishnavi-daggula04/resume-analyzer-bot.git
cd resume-analyzer-bot

Install dependencies:
pip install -r requirements.txt

Run the app:
streamlit run app.py

💼 Supported Roles
✅ Data Scientist, ML Engineer, Data Analyst

✅ Backend / Frontend / Full Stack Developer

✅ UI/UX Designer, Cloud / DevOps Engineer

✅ QA Engineer, Product Manager, and many more...

🧾 License
This project is licensed under the MIT License.

