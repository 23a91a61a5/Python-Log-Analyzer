import re  # Import regular expressions module for pattern matching


# Function to read raw log text and convert each valid line into a structured dictionary
def parse_logs(raw_text):
    logs = []  # Store parsed log entries here

    # Pattern:
    # 1) timestamp in format YYYY-MM-DD HH:MM:SS
    # 2) log level like INFO, WARNING, ERROR
    # 3) message text
    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+([A-Z]+)\s+(.*)"

    # Split the full text into separate lines
    for line in raw_text.splitlines():

        # Try to match each line with the log pattern
        match = re.match(pattern, line)

        # If the line matches, extract timestamp, level, and message
        if match:
            logs.append({
                "timestamp": match.group(1),
                "level": match.group(2),
                "message": match.group(3)
            })

    # Return the list of parsed log dictionaries
    return logs


# Function to count total logs and each log level
def generate_report(logs):
    # Initialize report with counters
    report = {
        "total_logs": len(logs),  # total number of valid log entries
        "INFO": 0,                # count of INFO logs
        "WARNING": 0,             # count of WARNING logs
        "ERROR": 0                # count of ERROR logs
    }

    # Loop through each parsed log entry
    for log in logs:

        # Get the log level from the entry
        level = log["level"]

        # Increase count if the level exists in the report
        if level in report:
            report[level] += 1

    # Return final summary report
    return report


# NEW: function to analyze a log file and return stats for the UI
def analyze_log_file(file_path):
    # Read the whole file
    with open(file_path, "r", errors="ignore") as f:
        raw_text = f.read()

    # Use your existing logic
    logs = parse_logs(raw_text)
    report = generate_report(logs)

    # Map report to names that are easy to show on the page
    return {
        "total_lines": report["total_logs"],
        "info_count": report["INFO"],
        "warning_count": report["WARNING"],
        "error_count": report["ERROR"],
        # You can extend this later (e.g., most_common_error)
        "most_common_error": "Not calculated",  # placeholder
    }
