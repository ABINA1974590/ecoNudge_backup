# SmartNudge - Sustainability Nudge App

[![Demo](screenshots/demo.png)](http://localhost:5000)

Personalized sustainability suggestions for hotel guests with Flask backend and modern HTML/CSS frontend.

## 🚀 Quick Start

```powershell
cd "C:/Users/GenAIKOCVISUSR31/Desktop/SmartNudge"
pip install -r requirements.txt
python app.py
```

- **Guest Portal**: http://localhost:5000
- **Manager Dashboard**: http://localhost:5000/dashboard

## ✨ Features

- 👤 Guest profile form (age, health, children, caregiver, preference)
- 🤖 Rule-based AI decision engine for personalized nudges
- 💬 Guest-friendly nudge display with opt-out
- 📊 Manager dashboard with guest types, nudges, CO2 impact
- 🎨 Beautiful glassmorphism UI, responsive design
- 📈 Synthetic demo data

## 🗄️ Project Structure

```
SmartNudge/
├── app.py                 # Flask app, AI logic, synthetic data
├── requirements.txt       # Dependencies
├── README.md             # This file
├── TODO.md               # Completed tasks
├── templates/
│   ├── base.html         # Layout
│   ├── guest_form.html   # Profile form
│   ├── guest_nudge.html  # Nudge display
│   └── dashboard.html    # Manager view
└── static/css/
    └── style.css         # Modern UI styles
```

## 📂 Git Repo Setup

1. **Install Git**: Download from [git-scm.com](https://git-scm.com)
2. **Restart VSCode/terminal**
3. **GitHub CLI**: `winget install --id GitHub.cli`
4. **Commands**:
```bash
cd "C:/Users/GenAIKOCVISUSR31/Desktop/SmartNudge"
git init
git add .
git commit -m "feat: complete SmartNudge sustainability app"
gh repo create SmartNudge --public --source=. --push --remote=origin
git push -u origin main
```

**Push to your repo**: https://github.com/ABINA1974590/GenAI.git

## 🎯 AI Logic

Rule-based engine personalizes based on:
- Age group → specific actions
- Children/caregiver → family tips
- Health → accessible suggestions
- Preference → effort level

## 📱 Screenshots

*Add screenshots after running*

## 🔮 Future

- Real ML model
- Database persistence
- Multi-language
- Analytics API

© 2024 SmartNudge - Green Stays Powered by AI
