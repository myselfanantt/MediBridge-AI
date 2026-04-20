# MediBridge AI Backend 🏥

This is the FastAPI-based backend for the MediBridge-AI platform, providing medical consultation, AI-driven symptom checking, and emergency services.

## 🚀 Features
- **Auth**: Flexible patient and doctor authentication.
- **AI Consultation**: Keyword-based symptom checker and medical chatbot.
- **Appointments**: Real-time appointment booking and management.
- **Emergency**: Real-time hospital and pharmacy location fetching using OpenStreetMap.
- **Digital Records**: Secure health record management.
- **Real-time**: WebSocket integration for instant chat and notifications.

## 🛠️ Tech Stack
- **Framework**: FastAPI (Python 3.12)
- **Database**: SQLite with SQLAlchemy ORM
- **AI**: Custom logic for medical diagnostics
- **Maps**: Overpass API (OpenStreetMap)

## 🏃 Running Locally

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Start the Server**:
   ```bash
   python -m uvicorn main:app --reload
   ```

3. **Access API Docs**:
   Go to `http://localhost:8000/docs` to see the interactive Swagger UI.
