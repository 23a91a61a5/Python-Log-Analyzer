"""
analyzer.py
-----------
Core module containing log parsing, filtering, statistics, and reporting logic.
This module is designed to be highly modular, readable, and beginner-friendly.
"""

import re
import os
import csv
import datetime

# Add a constant in analyzer.py: VALID_LEVELS
# Used for validating and filtering log levels throughout the application.
VALID_LEVELS = ["INFO", "WARNING", "ERROR", "DEBUG", "CRITICAL"]

# REGEX PARSING EXPLANATION:
# The regex pattern matches log entries following the standard pattern:
# "YYYY-MM-DD HH:MM:SS [LEVEL] Log message content"
#
# Break-down of components:
# ^                          - Assert start of the line.
# (\d{4}-\d{2}-\d{2})        - Match 4-digit year, 2-digit month, 2-digit day.
# ( )                        - Match single space.
# (\d{2}:\d{2}:\d{2})        - Match 2-digit hour, minute, second.
# (timestamp group combining date + time is captured by the outer parenthesis)
# \[([A-Z]+)\]               - Match uppercase words inside square brackets (the log LEVEL).
# (.*)                       - Match and capture the rest of the message (the log MESSAGE).
# $                          - Assert end of the line.
LOG_PATTERN = re.compile(r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}) \[([A-Z]+)\] (.*)$")

def ensure_sample_log_exists(file_path="sample.log"):
    """
    Startup Check: Checks if a log file exists. If it does not,
    automatically creates a minimal sample log file with standard valid entries.
    
    Args:
        file_path (str): File path to verify/create.
    """
    if not os.path.exists(file_path):
        default_entries = [
            "2026-05-29 09:00:00 [INFO] System boot process initiated.\n",
            "2026-05-29 09:00:05 [INFO] Core systems and kernel modules loaded successfully.\n",
            "2026-05-29 09:00:10 [INFO] Network interface eth0 up with IP 192.168.1.50.\n",
            "2026-05-29 09:01:15 [DEBUG] Checking database replica replication status...\n",
            "2026-05-29 09:01:20 [INFO] Database connection established successfully on replica master.\n",
            "2026-05-29 09:02:00 [INFO] User admin initiated login process from remote IP 192.168.1.100.\n",
            "2026-05-29 09:02:05 [INFO] User admin logged in successfully. Session SESS827361 created.\n",
            "2026-05-29 09:03:10 [DEBUG] Refreshing token cache maps...\n",
            "2026-05-29 09:05:00 [WARNING] Disk space usage is high: 88% capacity reached on partition /dev/sda1.\n",
            "2026-05-29 09:05:30 [INFO] Cache cleanup daemon started background garbage collection.\n",
            "2026-05-29 09:06:00 [INFO] Cache cleanup completed. Freed 142MB of temporary cache objects.\n",
            "2026-05-29 09:10:15 [CRITICAL] Internal power supply temperature exceeds safe threshold: 78C.\n",
            "This is an invalid malformed log line that does not match the regex pattern at all.\n",
            "2026-05-29 09:12:45 [WARNING] Failed login attempt for user guest from remote IP 192.168.1.105.\n",
            "2026-05-29 09:13:00 [WARNING] Failed login attempt for user guest from remote IP 192.168.1.105.\n",
            "2026-05-29 09:13:15 [ERROR] Login attempts limit exceeded for user guest. Account locked automatically.\n",
            "2026-05-29 09:14:00 [INVALID_LEVEL] This log line has an invalid level not present in VALID_LEVELS.\n",
            "2026-05-29 09:15:30 [INFO] Service web_server started listening on port 8080 successfully.\n",
            "2026-05-29 09:17:12 [DEBUG] Port forwarding set up completed on port 8080.\n",
            "2026-05-29 09:20:00 [ERROR] Database write transaction timed out. Transaction ID: TX_88192.\n",
            "2026-05-29 09:21:40 [INFO] Automatic database query optimization index scan initiated.\n",
            "2026-05-29 09:22:15 [ERROR] Failed to query database replica. Falling back to primary master instance.\n",
            "2026-05-29 09:23:05 [WARNING] Replication lag detected: replica is 12 seconds behind master.\n",
            "2026-05-29 09:25:00 [INFO] Backup service executed successfully. Archive saved as backup_20260529.zip.\n",
            "2026-05-29 09:27:14 [DEBUG] Starting index cleanups on table billing_details...\n",
            "2026-05-29 09:28:40 [INFO] API Gateway route configured successfully: /api/v1/billing -> port 8081.\n",
            "2026-05-29 09:29:10 [INFO] User supervisor checked billing endpoint from IP 192.168.1.200.\n",
            "2026-05-29 09:30:15 [WARNING] API Gateway response latency spike detected: average 450ms.\n",
            "Another completely malformed line with no timestamp structure whatsoever.\n",
            "2026-05-29 09:32:00 [INFO] Automated hourly system health diagnostics passed successfully.\n"
        ]
        
        # EXCEPTION HANDLING: Trap any permission/IO issues while writing the new file
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.writelines(default_entries)
        except Exception as e:
            # Propagate error with a friendly description
            raise IOError(f"Could not create default sample log file: {e}")

def parse_log_line(line):
    """
    Parses a single line of log text.
    
    Args:
        line (str): A raw line from a log file.
        
    Returns:
        dict: A dictionary containing 'timestamp', 'level', and 'message' if valid.
        None: If the line does not match the pattern or has an invalid log level.
    """
    cleaned_line = line.strip()
    if not cleaned_line:
        return None  # Skip purely empty lines silently
    
    # Apply regex match
    match = LOG_PATTERN.match(cleaned_line)
    if not match:
        return None  # Malformed line (does not match expected format)
    
    timestamp = match.group(1)
    level = match.group(2).upper()
    message = match.group(3)
    
    # Validate against our list of authorized log levels (VALID_LEVELS)
    if level not in VALID_LEVELS:
        return None  # Skip logs with non-conforming levels (e.g., [INVALID_LEVEL])
        
    return {
        "timestamp": timestamp,
        "level": level,
        "message": message
    }

def read_log_file(file_path):
    """
    Reads a log file and processes it line by line.
    
    Args:
        file_path (str): Absolute or relative path to the log file.
        
    Returns:
        tuple: (list of parsed log dicts, int count of invalid lines skipped)
        
    Raises:
        FileNotFoundError: If the file does not exist.
        PermissionError: If there are insufficient permissions to read the file.
        IsADirectoryError: If the path points to a directory instead of a file.
    """
    # EXCEPTION HANDLING & INPUT VALIDATION:
    # We verify file existence, file-vs-directory mismatches, and permissions.
    # This prevents the application from crashing and allows showing helpful dialogs.
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file path '{file_path}' does not exist.")
    
    if os.path.isdir(file_path):
        raise IsADirectoryError(f"The path '{file_path}' is a directory, not a file.")
        
    logs = []
    invalid_count = 0
    
    # Open and process the file
    # Using utf-8 encoding to support diverse text characters and avoid crashing
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            # Skip completely empty lines without counting them as invalid
            if not line.strip():
                continue
                
            parsed = parse_log_line(line)
            if parsed is None:
                # Add invalid log line tracking while parsing
                invalid_count += 1
            else:
                logs.append(parsed)
                
    return logs, invalid_count

def filter_logs(logs, level=None, keyword=None, sort_by_timestamp=False):
    """
    Filters and optionally sorts a list of logs.
    
    Args:
        logs (list): List of parsed log dictionaries.
        level (str, optional): Log level to filter by (e.g. 'INFO').
        keyword (str, optional): Keyword substring to search for in log messages.
        sort_by_timestamp (bool, optional): Whether to sort logs chronologically.
        
    Returns:
        list: Filtered and optionally sorted log dictionaries.
    """
    filtered = []
    
    for log in logs:
        # Check level match if a level is specified
        if level:
            if log["level"].upper() != level.upper():
                continue
                
        # Check case-insensitive keyword match if a keyword is specified
        if keyword:
            if keyword.lower() not in log["message"].lower():
                continue
                
        filtered.append(log)
        
    # Add optional timestamp-based sorting for logs
    if sort_by_timestamp:
        # Sorting logs using python lambda key pointing to timestamp string values
        filtered.sort(key=lambda x: x["timestamp"])
        
    return filtered

def calculate_statistics(logs, invalid_count):
    """
    Computes summary statistics for parsed log data.
    
    Args:
        logs (list): List of parsed valid log dictionaries.
        invalid_count (int): Count of malformed/invalid lines.
        
    Returns:
        dict: A statistics summary.
    """
    # Initialize counts for all valid levels to zero
    level_counts = {level: 0 for level in VALID_LEVELS}
    
    # Populate counts based on actual logs
    for log in logs:
        level = log["level"]
        if level in level_counts:
            level_counts[level] += 1
            
    total_valid = len(logs)
    total_entries = total_valid + invalid_count
    
    return {
        "total_entries": total_entries,
        "total_valid": total_valid,
        "invalid_skipped": invalid_count,
        "level_counts": level_counts
    }

def generate_txt_report(stats, filtered_logs, output_path="report.txt"):
    """
    Generates a beautifully formatted text report.
    
    Args:
        stats (dict): Statistics calculated from the active log set.
        filtered_logs (list): The list of logs (filtered) to append as details.
        output_path (str): File path where the TXT report will be saved.
    """
    # Add professional report headers in TXT reports.
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    report_lines = [
        "====================================",
        "      PYTHON LOG ANALYZER REPORT      ",
        "====================================",
        f"Generated On: {now}",
        "",
        "------------------------------------",
        "         SUMMARY STATISTICS         ",
        "------------------------------------",
        f"Total Entries Processed : {stats['total_entries']}",
        f"Valid Log Entries       : {stats['total_valid']}",
        f"Invalid Lines Skipped   : {stats['invalid_skipped']}",
        "",
        "LOG LEVEL BREAKDOWN:"
    ]
    
    # List counts for each valid level
    for level, count in stats["level_counts"].items():
        report_lines.append(f"  - {level:<10}: {count}")
        
    report_lines.extend([
        "",
        "------------------------------------",
        "        FILTERED LOG ENTRIES        ",
        "------------------------------------",
        f"Total Logs in Segment: {len(filtered_logs)}",
        "",
        f"{'TIMESTAMP':<20} | {'LEVEL':<8} | {'MESSAGE'}"
    ])
    report_lines.append("-" * 80)
    
    for log in filtered_logs:
        report_lines.append(f"{log['timestamp']:<20} | {log['level']:<8} | {log['message']}")
        
    # EXCEPTION HANDLING: Trap any file writing errors
    try:
        with open(output_path, "w", encoding="utf-8") as file:
            file.write("\n".join(report_lines) + "\n")
    except Exception as e:
        raise IOError(f"Could not generate text report: {e}")

def generate_csv_report(filtered_logs, output_path="report.csv"):
    """
    Exports filtered logs to a standard CSV file.
    
    Args:
        filtered_logs (list): List of log dictionaries.
        output_path (str): File path where the CSV report will be saved.
    """
    headers = ["Timestamp", "Level", "Message"]
    
    # EXCEPTION HANDLING: Trap any spreadsheet write interruptions or locks
    try:
        with open(output_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            for log in filtered_logs:
                writer.writerow([log["timestamp"], log["level"], log["message"]])
    except Exception as e:
        raise IOError(f"Could not generate CSV report: {e}")

def generate_visualization(stats, output_path="report_chart.png"):
    """
    VISUALIZATION GENERATION EXPLANATION:
    Creates a visual bar chart of log level occurrences using matplotlib.
    It takes the calculated counts for each log level, maps them into a vertical
    bar representation, styles it with Harmonious premium colors, overlays exact data
    counts on top of the bars, and saves the plot as a PNG image.
    
    If matplotlib is not installed, it catches ImportError and returns False gracefully.
    
    Args:
        stats (dict): Statistics dict containing level counts.
        output_path (str): File path where the visual PNG chart will be saved.
        
    Returns:
        bool: True if successful, False if matplotlib could not be loaded.
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        # Graceful fallback: return False so calling code can warn the user without crashing
        return False

    # Extract log levels and their respective counts
    levels = list(stats["level_counts"].keys())
    counts = list(stats["level_counts"].values())
    
    # Skip rendering if there are no logs at all to prevent empty plots
    if sum(counts) == 0:
        return False
        
    # Use Harmonious premium colors matching modern UI systems
    colors = {
        "INFO": "#2ecc71",     # Premium Soft Emerald Green
        "WARNING": "#f1c40f",  # Vibrant Soft Sunflower Yellow
        "ERROR": "#e74c3c",    # Deep Soft Alizarin Red
        "DEBUG": "#3498db",    # Sleek Soft Peter River Blue
        "CRITICAL": "#9b59b6"  # Premium Soft Amethyst Purple
    }
    
    bar_colors = [colors.get(level, "#95a5a6") for level in levels]

    # Initialize plt figure with proper layout
    plt.figure(figsize=(8, 5))
    
    # Create the bar chart
    bars = plt.bar(levels, counts, color=bar_colors, edgecolor="#2c3e50", width=0.6)
    
    # Modern grid layout
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    # Adding precise counts on top of each bar
    for bar in bars:
        height = bar.get_height()
        if height > 0:
            plt.annotate(f'{height}',
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Styling title and labels with premium typographic selections
    plt.title("Distribution of Log Levels", fontsize=14, fontweight="bold", pad=15, color="#2c3e50")
    plt.xlabel("Log Level", fontsize=11, fontweight="bold", labelpad=10, color="#2c3e50")
    plt.ylabel("Occurrences", fontsize=11, fontweight="bold", labelpad=10, color="#2c3e50")
    
    # Tight layout ensures labels do not overlap boundaries
    plt.tight_layout()
    
    # Save the chart to disk
    # EXCEPTION HANDLING: Trap image save issues (e.g. read-only folder locks)
    try:
        plt.savefig(output_path, dpi=300)
    except Exception as e:
        plt.close()
        raise IOError(f"Could not save visual chart image: {e}")
        
    plt.close()
    return True