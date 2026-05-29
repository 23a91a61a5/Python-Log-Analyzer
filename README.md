\# 🔍 Professional Python Log Analyzer \& Dashboard Engine



An interactive, premium, and beginner-friendly \*\*Log Analyzer \& Dashboard Engine\*\* written in Python. This utility processes system and application log files line-by-line using regular expressions, tracks and recovers from malformed/invalid inputs, aggregates statistics, outputs analytical charts, monitors log files in real-time (`tail -f`), and provides a modern Tkinter GUI dashboard. 



This project is structured specifically to serve as a resume-worthy demonstration of modular programming, exception handling, data parsing, and user interface design.



\---



\## 🚀 Professional Highlights 

\*   \*\*Robust Regex Parser\*\*: Reads files safely using regular expressions to extract timestamp, level, and message details.

\*   \*\*Log Level Validation\*\*: Cross-checks logs against a constant list of validated levels (`INFO`, `WARNING`, `ERROR`, `DEBUG`, `CRITICAL`).

\*   \*\*Invalid Log Line Tracking\*\*: Flags and counts malformed or unauthorized logs, continuing execution without program crashes.

\*   \*\*Interactive Search \& Filters\*\*: Search log files dynamically by specific log level, substring keywords, and optional chronological sorting.

\*   \*\*Colored Terminal Diagnostics\*\*: Utilizes `colorama` to print log levels in consistent colors (Green for `INFO`, Yellow for `WARNING`, Red for `ERROR`, Cyan for `DEBUG`, Magenta for `CRITICAL`).

\*   \*\*Multi-Format Export\*\*: Generates professional text summaries with custom headers (`report.txt`) and exports structured CSV data (`report.csv`).

\*   \*\*Visual Data Analytics\*\*: Compiles log stats and plots premium charts (`report\_chart.png`) via `matplotlib`.

\*   \*\*Live Log Monitoring\*\*: Includes a real-time event watcher (`tail -f`) that instantly catches and highlights new log additions.

\*   \*\*Tkinter Desktop Dashboard\*\*: Exposes a gorgeous desktop window with tabular views, filtering controls, side statistical panels, and integrated chart models.

\*   \*\*Complete Error Handling\*\*: Fully handles missing files, path issues, directories, and permission limits using `try-except` traps.



\---



\## 🛠️ Enterprise Concepts Demonstrated



1\.  \*\*Strict Separation of Concerns\*\*: Isolates core business logic (`analyzer.py`) from multiple visual presentation layers (`main.py`, `gui.py`).

2\.  \*\*Defensive Programming\*\*: Incorporates deep nested exception blocks (`FileNotFoundError`, `PermissionError`, `ImportError`, and `IOError`) preventing crash states and enabling smooth fallbacks.

3\.  \*\*Real-Time Data Streaming\*\*: Implements polling tail listeners (`tail -f`) avoiding resource starvation using calculated system sleeps (`time.sleep`).

4\.  \*\*UI/UX Packaging and Compatibility\*\*: Utilizes Pillow to guarantee cross-system image rendering stability with automatic fallback loaders for standard libraries.



\---



\## 📁 Folder Structure



```text

log-analyzer-python/

│

├── main.py              # Main interactive CLI application (uses colorama)

├── analyzer.py          # Core parser, filter logic, stats, and reports API

├── gui.py               # Tkinter Desktop Dashboard wrapper (uses Pillow)

├── sample.log           # Realistic system log file with valid \& invalid lines (auto-created if missing)

├── requirements.txt     # Third-party dependency definitions

└── README.md            # Highly descriptive, resume-worthy project documentation ```



