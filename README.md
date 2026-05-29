Python Log Analyzer
Overview

Log Analyzer is a Python-based tool that reads and analyzes log files to identify errors, warnings, and important system events. It helps in quickly understanding system behavior and debugging issues.

✨ Features
Reads and parses log files
Detects log levels (INFO, WARNING, ERROR)
Counts total logs and categories
Filters logs by keywords or level
Generates simple summary reports

🛠 Tech Stack
Python 3
File Handling
Regular Expressions

📁 Project Structure
log-analyzer/
│── main.py
│── analyzer.py
│── parser.py
│── sample.log
│── README.md

▶️ How to Run
python main.py

📥 Input Format
[INFO] Application started
[WARNING] Low disk space
[ERROR] Connection failed

📊 Output
Total log count
INFO / WARNING / ERROR counts
Filtered results based on input
