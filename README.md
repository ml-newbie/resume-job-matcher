
---


# 📄 AI Resume ↔ Job Description Matcher

A Streamlit-based AI-powered application that evaluates how well a candidate’s resume matches a job description. It uses LLM-driven analysis to extract skills, compare experience, and generate a structured hiring report with visual insights.

🌐 **Live App:** https://resume-job-matcher-6ihr.onrender.com/

---

## 🚀 Features

- 📤 Upload resume and job description (PDF format)
- 🤖 AI-powered matching using CrewAI workflow
- 📊 Detailed scoring across multiple dimensions:
  - Skills Match
  - Experience Match
  - Technical Alignment
  - Role Readiness
- 📈 Radar chart visualization of candidate fit
- 🧠 Extracted insights:
  - Matching & missing skills
  - Critical gaps
  - Pros & cons per category
- 🎯 Recruiter-focused output:
  - Red flags
  - Suggested interview questions
  - Culture fit estimation
- 📑 Executive summary of candidate evaluation
- 🔐 Password-protected access

---

## 🧠 How It Works

1. Upload:
   - Candidate Resume (PDF)
   - Job Description (PDF)

2. The system:
   - Extracts text using PDF parser (`read_pdf`)
   - Runs AI analysis pipeline (`run_resume_matching`)
   - Evaluates candidate-job alignment

3. Outputs:
   - Structured hiring report
   - Visual radar chart
   - Recruiter insights

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Visualization:** Plotly
- **AI Workflow:** CrewAI
- **Backend Logic:** Python
- **PDF Processing:** Custom PDF reader utility

---

## 📦 Project Structure

```

.
├── app.py                  # Main Streamlit application
├── pdf_reader.py          # PDF text extraction
├── run_workflow.py        # AI matching workflow (CrewAI)
├── get_keys.py            # Secret management
├── requirements.txt       # Dependencies
└── README.md

```

---

## 🔐 Environment Variables

The app requires the following secret:

```

APP_PASSWORD=your_password_here

````

You can configure it in your environment or secret manager.

---

## ▶️ Run Locally

### 1. Clone the repository
```bash
git clone https://github.com/your-username/resume-job-matcher.git
cd resume-job-matcher
````

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Mac/Linux
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Streamlit app

```bash
streamlit run app.py
```

---

## 🌐 Deployment

This project is deployed on **Render**:
👉 [https://resume-job-matcher-6ihr.onrender.com/](https://resume-job-matcher-6ihr.onrender.com/)

---

## ⚠️ Notes

* Only PDF uploads are supported.
* Ensure both resume and job description are provided before running analysis.
* App access is protected by a password prompt.

---

## 👨‍💻 Author

Developed by **John M.**
© 2026

---

## 📜 License

This project is open-source and available under the MIT License.




