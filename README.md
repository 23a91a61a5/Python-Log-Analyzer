

# 🧾 Python Log Analyzer – Web-based Log Analysis System

## 📌 Overview

Python Log Analyzer is a web-based log analysis application that helps users upload, parse, and visualize log files through an interactive interface.  
The system uses a Django backend, a Flask log-processing service, and a modern frontend to deliver insights such as errors, warnings, statistics, and patterns from raw log data.  
This project demonstrates full-stack development with Python, REST APIs, file handling, and basic data analytics for real-world log files.

***

## ✨ Features

### 📁 Log Upload & Management

- Upload log files (for example, application logs or server logs) from the browser to the server.  
- Store uploaded files in a dedicated `uploads` directory for later processing.  

### 📊 Log Analysis

- Extract key information such as timestamps, log levels (INFO, WARNING, ERROR), and messages.  
- Compute useful metrics like total log entries, error counts, and other statistics (depending on your analyzer implementation).  
- Support modular analysis logic inside the `analyzer` module so you can extend it easily.  

### 🌐 Web Interface

- Simple, user-friendly **frontend** to select and upload log files and view results.  
- Designed to communicate with the Django backend via HTTP APIs.  

### 🔗 Service-Oriented Architecture

- **Django backend** handles routes, API endpoints, and database integration if needed.  
- **Flask log service** focuses on actual log parsing and analysis, keeping concerns separate.  

### 🧰 Developer Friendly

- Clear project structure with separate folders for backend, services, frontend, and analyzer logic.  
- Uses common tools and technologies that are easy to extend in future (Django, Flask, HTML/CSS/JS).  

***

## 🏗️ Project Architecture

High-level flow:

User Browser  
⬇️  
**Frontend (HTML/CSS/JavaScript)**  
⬇️  
**Django Backend (REST API)**  
⬇️  
**Flask Log Service (Log parsing & analysis)**  
⬇️  
**Analyzer module (core log analysis logic)**  
⬇️  
Processed Log Insights (counts, errors, patterns, etc.)



***

## 🛠️ Technologies Used

### Frontend

- HTML  
- CSS  
- JavaScript  

### Backend

- Django  
- Django REST Framework (if used)  

### Log Service

- Flask  

### Core Logic

- Custom Python modules in the `analyzer` package  

### Database (optional / if configured)

- SQLite (default for Django)  

### Tools

- Git & GitHub  
- VS Code (recommended)  



***

## 📂 Project Structure

Your repository structure on GitHub: 

```text
Python-Log-Analyzer/
├── analyzer/             # Core log analysis logic (parsers, utilities, etc.)
├── django_backend/       # Django project and apps (views, URLs, APIs)
├── flask_log_service/    # Flask service exposing log processing endpoints
├── frontend/             # Static frontend (HTML, CSS, JS)
├── uploads/              # Folder for uploaded log files
├── .env                  # Environment variables (not for production)
├── .gitignore            # Git ignore rules
├── README.md             # Project documentation
└── requirements.txt      # Python dependencies
```

You can adjust details inside each folder description to match your exact code.

***

## ⚙️ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/23a91a61a5/Python-Log-Analyzer.git
cd Python-Log-Analyzer
```


### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

(Use `source venv/bin/activate` on Linux/macOS.)

### 3. Install Dependencies

Either install from `requirements.txt` (if you maintain it):

```bash
pip install -r requirements.txt
```

Or install manually as needed (Django, Flask, etc.):

```bash
pip install django djangorestframework django-cors-headers flask flask-cors
```

***

## 🚀 Running the Application

You likely need two (or three) terminals open.

### Terminal 1 – Run Django Backend

```bash
cd django_backend
python manage.py migrate
python manage.py runserver
```

Server (default):  
`http://127.0.0.1:8000/`

### Terminal 2 – Run Flask Log Service

```bash
cd flask_log_service
python app.py
```

Server (example):  
`http://127.0.0.1:5000/`

### Frontend – Open UI

Open the `frontend/index.html` file in your browser (either directly by double-clicking or via a simple static server).  
The frontend should call the Django backend APIs, which in turn can use the Flask log service and analyzer logic. 

***

## 🧪 Testing

Example scenario:

- Upload a sample log file (for example `sample.log` with multiple log levels).  
- View the analysis results in the UI: counts of errors, warnings, timelines, or any metrics you implemented.  
- Verify that the Django backend and Flask service both run without errors in their terminals.  

You can also test API endpoints using tools like Postman or curl if your Django/Flask apps expose JSON APIs.

***

## 👨‍💻 Developer

Final Year / Internship Project  
Built using Python, Django, Flask, and full-stack web technologies for practical log analysis.

***

If you tell me exactly how your analyzer works (what stats it computes), I can further customize the Features and Testing sections to perfectly match your implementation.
