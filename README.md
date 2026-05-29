# 🔍 Python Log Analyzer & Dashboard Engine

A modular and beginner-friendly **Log Analyzer Dashboard** built with Python.  
This application processes system and application log files using regular expressions, detects malformed entries, generates statistics, exports reports, visualizes log distributions, and provides an interactive Tkinter GUI dashboard.

The project demonstrates practical Python concepts including file handling, regex parsing, exception handling, data visualization, modular architecture, and GUI development.

---

## 🚀 Features

- ✅ Parse log files using Regular Expressions (Regex)
- ✅ Validate log levels (`INFO`, `WARNING`, `ERROR`, `DEBUG`, `CRITICAL`)
- ✅ Detect and skip malformed log entries safely
- ✅ Filter logs by:
  - Log Level
  - Keywords
  - Timestamp Sorting
- ✅ Generate professional TXT reports
- ✅ Export structured CSV reports
- ✅ Create graphical log analysis charts using `matplotlib`
- ✅ Interactive Tkinter GUI Dashboard
- ✅ Real-time log monitoring support (`tail -f`)
- ✅ Strong exception handling and recovery mechanisms
- ✅ Beginner-friendly modular code structure

---

## 🛠️ Technologies Used

- Python 3
- Tkinter
- Regular Expressions (`re`)
- Matplotlib
- Colorama
- Pillow (PIL)
- CSV Handling
- File System Operations

---

## 📁 Project Structure

```text
Python-Log-Analyzer/
│
├── analyzer.py          # Core parsing, filtering, statistics, and report engine
├── main.py              # Command-line interface version
├── gui.py               # Tkinter GUI dashboard
├── sample.log           # Sample log file
├── requirements.txt     # Project dependencies
├── README.md            # Project documentation
│
├── report.txt           # Generated TXT report
├── report.csv           # Generated CSV report
└── report_chart.png     # Generated chart visualization
```

---

## ⚙️ Installation

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/23a91a61a5/Python-Log-Analyzer.git
cd Python-Log-Analyzer
```

### 2️⃣ Install Dependencies

```bash
py -m pip install -r requirements.txt
```

---

## ▶️ Running the Project

### Run GUI Version

```bash
py gui.py
```

### Run CLI Version

```bash
py main.py
```

---

## 📊 Functionalities

### 🔹 Log Parsing

The analyzer extracts:

- Timestamp
- Log Level
- Message Content

using Regex pattern matching.

### 🔹 Statistics Dashboard

Displays:

- Total Entries
- Valid Logs
- Invalid Logs
- Log Level Counts

### 🔹 Report Generation

Exports:

- TXT Summary Reports
- CSV Structured Reports

### 🔹 Visualization

Generates bar charts representing log level distribution using `matplotlib`.

---

## 🧠 Concepts Demonstrated

- Modular Programming
- Object-Oriented GUI Design
- Exception Handling
- Regex Parsing
- File Processing
- Data Visualization
- CSV Exporting
- Tkinter Desktop Applications

---

## 📦 Requirements

- Python 3.10+
- matplotlib
- pillow
- colorama

---

## ❌ Exception Handling Covered

The application safely handles:

- Missing files
- Invalid file paths
- Directory selection mistakes
- Permission errors
- Invalid log formats
- Missing dependencies

without crashing the program.

---

## 📸 Sample Output

- GUI Dashboard with Log Table
- Statistics Sidebar
- CSV/TXT Export Files
- Log Distribution Chart

---

## 👩‍💻 Author

Developed by Lova Laxmi as a Python development project.

---
