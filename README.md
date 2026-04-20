# MediBridge AI 🏥✨

Welcome to the **MediBridge AI** repository! This is a state-of-the-art, comprehensive, AI-powered healthcare platform designed to seamlessly connect patients, doctors, and pharmacies.

## 🚀 Project Overview

MediBridge AI aims to revolutionize health access and record management through an intuitive digital ecosystem. The project is split into three main components: a fully-functional Web Application, a native Android Application, and a robust Python AI Backend.

---

## 📂 Project Structure

This repository is organized into the following major modules:

### 1. 🌐 Web Frontend (React + Vite)
Located in `medibridge-connect-main/medibridge-connect-main/src/`
The web app is a responsive, feature-rich dashboard built with React. Key features include:
- **Role-Based Dashboards**: Segregated views for Patients and Doctors.
- **Symptom Checker**: A smart interface where users can input symptoms and get AI-driven health insights.
- **Appointments Management**: Effortlessly book, track, and manage doctor appointments.
- **Medicine Tracking**: Order and view prescriptions seamlessly.
- **Health Records Viewer**: Access medical history safely.

### 2. 📱 Mobile Application (Native Android)
Located in `medibridge-connect-main/native-android/`
The native mobile app is built in **Kotlin** and utilizes **Jetpack Compose** for a modern, fluid user interface.
- Includes smooth navigation (`AppNavigation.kt`), dynamic Splash Screens, and Role Selection.
- Uses `MediBridgeApi.kt` for efficient, asynchronous data fetching across REST APIs.
- Fully synchronized dynamically with the user's web account data.

### 3. 🧠 Smart Backend & APIs (Python / FastAPI)
Located in `medibridge-connect-main/medibridge-connect-main/backend/`
The backend handles the heavy lifting, database operations, and AI intelligence.
- **AI Routers (`ai_routes.py`)**: Integrates directly with LLMs (Large Language Models) to power the symptom checker and health analytics.
- **Pharmacy Models (`pharmacy_model.py`)**: A structured data pipeline to track pharmaceutical inventories, medicinal availability, and deliveries.
- **Real-Time Sync**: Fully RESTful interface to ensure that any action taken on Web immediately reflects in Mobile.

---

## 🛠️ Tech Stack & Technologies

*   **Frontend**: React, TypeScript, TailwindCSS (assumed), Vite.
*   **Mobile**: Kotlin, Android Studio, Jetpack Compose, Capacitor (for hybrid fallbacks).
*   **Backend Application**: Python (FastAPI), WebSockets for real-time Sync.
*   **Version Control**: Git / GitHub.

---

## ⚙️ Getting Started

### Prerequisites
- Node.js (v18+)
- Python (v3.9+)
- Android Studio (for mobile compilation)

### Running the Web Application
1. Navigate to the web folder: `cd medibridge-connect-main/medibridge-connect-main`
2. Install dependencies: `npm install`
3. Start the dev server: `npm run dev`

### Running the Python Backend
1. Navigate to the backend directory: `cd medibridge-connect-main/medibridge-connect-main/backend`
2. Activate your Virtual Environment: `python -m venv venv` and `venv\Scripts\activate`
3. Install Python requirements: `pip install -r requirements.txt`
4. Start the API server!

### Running the Android App
1. Open the `medibridge-connect-main/native-android/` folder in Android Studio.
2. Let Gradle sync and resolve project dependencies.
3. Build and launch on an emulator or a connected physical Android device.

---

## 📖 Features at a Glance

*   **Real-time AI Consultations:** Powered by the smart backend modules.
*   **Robust Role System:** Safely separating the scopes and privacy of doctors and patients.
*   **Cross-Platform Sync:** Start an action on the React UI and finish it on your Native Android Device.
*   **Secure API Integrations:** Making sure your health records are completely protected.

### Contributing
Given this is a private/personal repo, ensure all configurations (like your local `node_modules` and Python `venv`) are excluded in your `.gitignore` prior to committing.

---

*Built with ❤️ for a healthier future.*