import re


def parse_logs(raw_text):
    logs = []

    pattern = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s+([A-Z]+)\s+(.*)"

    for line in raw_text.splitlines():

        match = re.match(pattern, line)

        if match:
            logs.append({
                "timestamp": match.group(1),
                "level": match.group(2),
                "message": match.group(3)
            })

    return logs


def generate_report(logs):

    report = {
        "total_logs": len(logs),
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0
    }

    for log in logs:

        level = log["level"]

        if level in report:
            report[level] += 1

    return report