🧾 Python Log Analyzer
📌 Overview

Python Log Analyzer is a lightweight tool designed to read, parse, and analyze log files. It helps in identifying system events such as errors, warnings, and informational messages. This makes it easier to debug applications, monitor system behavior, and generate quick summaries from large log datasets.

✨ Features
Reads and processes log files efficiently
Detects different log levels such as INFO, WARNING, ERROR
Counts total number of logs and category-wise distribution
Filters logs based on keywords or log level
Generates structured summary reports for quick analysis
Helps in debugging and system monitoring
🛠 Tech Stack
Python 3.x
File Handling (open/read operations)
Regular Expressions (re module)
Basic data structures (lists, dictionaries)
📁 Project Structure
log-analyzer/
│── main.py          # Entry point of the application
│── parser.py        # Handles log parsing logic
│── analyzer.py      # Performs analysis on parsed logs
│── sample.log       # Sample log file for testing
│── README.md        # Project documentation
▶️ How to Run
Step 1: Clone or download the project
git clone <repo-link>
cd log-analyzer
Step 2: Run the program
python main.py
📥 Input Format

The tool expects log entries in a standard format like:

[INFO] Application started successfully
[WARNING] Low disk space detected
[ERROR] Failed to connect to database
[INFO] User logged in
📊 Output

After analysis, the tool generates:

Total number of log entries
Count of INFO logs
Count of WARNING logs
Count of ERROR logs
Filtered log results (based on user input or keywords)
Summary report for quick understanding
🧠 Working Logic (Simple Flow)
Read log file line by line
Parse each line using pattern matching
Identify log level (INFO / WARNING / ERROR)
Store and categorize logs
Perform analysis (counting + filtering)
Display results in structured format
