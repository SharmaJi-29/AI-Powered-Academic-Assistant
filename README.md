# 🎓 AI-Powered Academic Assistant
AI-Powered Academic Assistant is an intelligent desktop application that helps students study smarter, not harder. 
It integrates AI-based summarization, visual question solving, personalized study planning, and interactive academic assistance in a single unified platform.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![KivyMD](https://img.shields.io/badge/UI-KivyMD-green)
![NLP](https://img.shields.io/badge/NLP-Text%20Processing-orange)
![LLM](https://img.shields.io/badge/LLM-Ollama%20%7C%20Transformers-purple)
![OCR](https://img.shields.io/badge/OCR-Image%20%7C%20PDF-yellow)
![StudyPlanner](https://img.shields.io/badge/Feature-AI%20Study%20Planner-cyan)
![Domain](https://img.shields.io/badge/Domain-Education%20AI-red)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-Academic%20Use-lightgrey)

---
## 📌 Table of Contents
- [Overview](#📖-Overview)
- [Key Features](#✨-Key-Features)￼
- [System Architecture](#🧠-System-Architecture)￼
- [Tech Stack](#🛠-Tech-Stack)
- [Project Structure](#📂-Project-Structure)￼
- [Installation & Setup](#⚙️-Installation-&-Setup)￼
- [How to Run](#▶️-How-to-Run)￼
- [Application Workflow](#🔄-Application-Workflow)￼
- [Modules Explanation](#🧩-Modules-Explanation)￼
- [Screenshots](#🖼-Screenshots)￼
- [Future Enhancements](#🚀-Future-Enhancements)￼
- [Contribution Guidelines](#🤝-Contribution-Guidelines)￼
- [License](#📜-License)￼

---

## 📖 Overview
The AI-Powered Academic Assistant is designed to support students in their daily academic activities by leveraging Artificial Intelligence and NLP.

It provides:
- Automated document summarization
- Visual question solving using images/PDFs
- AI-generated personalized study plans
- A structured study planner with scheduling
- Secure login & user management

This project is ideal for:
- College students
- Exam aspirants
- Research-oriented learners
- AI-based academic projects

---

## ✨ Key Features
1. AI Document Summarizer
2. Visual Question Answering (Image / PDF based)
3. AI Study Planner (Daily & Scheduled Plans)
4. Interactive Ask-AI Chat Assistant
5. Login & Registration System
6. Local Database Storage (SQLite)
7. Modern UI with KivyMD
8. Offline-friendly Architecture

---

## 🧠 System Architecture
```bash
User Interface (KivyMD)
        |
        v
AI Processing Layer
(NLP | LLM | OCR | RAG)
        |
        v
Local Database (SQLite)
        |
        v
User Data | Study Plans | History
```
---

## 🛠 Tech Stack
| Category | Technology |
|--------|------------|
| Language | Python |
| UI Framework | Kivy & KivyMD |
| AI / NLP | Ollama Phi, Transformers|
| OCR | Tesseract / OpenCV |
| Database | SQLite |
| File Handling | PDF, Image, Text |
| OS Support | Windows / macOS / Linux |

---

## 📂 Project Structure
```bash
AI-Powered-Academic-Assistant/
│
├── splash.py                  # Splash screen
├── login.py                   # Login screen
├── register.py                # Registration screen
├── main.py                    # Main dashboard
├── database.py                # Database operations
├── users.db                   # SQLite database
│
├── summerizer.py              # AI document summarizer
├── ask_ai.py                  # AI chatbot
├── question_solving.py        # Visual Q&A module
│
├── studyplanner.py            # Study planner logic
├── studyplanner.kv            # Study planner UI
├── study_plan.json            # Generated plans
├── daily_plan.json            # Daily plans
├── study_tasks.json           # Task storage
│
├── academic.kv                # Main UI design
├── messaging_service.py       # Notifications & alerts
│
└── README.md                  # Project documentation
```
---

## ⚙️ Installation & Setup

**1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-username/AI-Powered-Academic-Assistant.git
cd AI-Powered-Academic-Assistant
```
**2️⃣ Create Virtual Environment (Recommended)**
```bash
python -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate         # Windows
```
**3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```
*Make sure Kivy, KivyMD, OpenCV, and NLP libraries are installed properly.*

---

## ▶️ How to Run
```bash
python main.py
```
*The application will launch with the Splash Screen → Login → Home Dashboard flow.*

---

## 🔄 Application Workflow
1. Splash Screen
2. User Login / Registration
3. Main Dashboard
4. Choose Module:
  - Summarizer
  - Ask AI
  - Visual Question Solver
  - Study Planner
5. AI processes input
6. Results stored locally
7. User receives structured output

---

## 🧩 Modules Explanation

**📘 AI Summarizer**
- Upload PDF / Text
- Generates concise academic summaries
- Useful for revision & notes

**🖼 Visual Question Solver**
- Upload image or scanned question
- OCR + AI reasoning
- Step-by-step explanation
  
**🗓 Study Planner**
- Personalized AI-generated study plans
- Daily & scheduled planning
- Stored in JSON format

**💬 Ask-AI Assistant**
- Academic Q&A chatbot
- Concept explanations
- Exam preparation support

---

## 🖼 Screenshots
![Splash Screen](screenshots/splash.png)
```bash
screenshots/
├── splash.png
├── login.png
├── dashboard.png
├── summarizer.png
├── study_planner.png
```
---

## 🚀 Future Enhancements
- 🔔 Smart reminders & notifications
- ☁️ Cloud sync (Firebase)
- 📱 Mobile version (Flutter)
- 📊 Analytics & progress tracking
- 🔐 Blockchain-based data security
- 🎯 Adaptive learning recommendations

---

## 🤝 Contribution Guidelines

Contributions are welcome!
1. Fork the repository
2. Create a new branch
3. Commit your changes
4. Open a Pull Request

*Please follow clean code practices and add proper documentation.*

---

## 📜 License

This project is licensed under the MIT License.
You are free to use, modify, and distribute it for academic and personal use.

---

## 👨‍💻 Author

**Mrityunjay Sharma**
AI & Software Engineering Enthusiast
*📧 Feel free to connect for collaboration or research projects*

---

*⭐ If you like this project, don’t forget to star the repository!**
