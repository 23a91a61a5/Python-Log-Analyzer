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
        "INFO": 0,               # count of INFO logs
        "WARNING": 0,            # count of WARNING logs
        "ERROR": 0               # count of ERROR logs
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
