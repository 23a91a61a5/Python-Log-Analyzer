def analyze_log(data: str):
    """
    Basic log analysis.
    - Counts total lines
    - Counts lines containing 'ERROR' or 'WARNING'
    - Shows the first error line (if any)
    """

    lines = data.splitlines()

    error_lines = [line for line in lines if "ERROR" in line]
    warning_lines = [line for line in lines if "WARNING" in line]

    result = {
        "total_lines": len(lines),
        "error_count": len(error_lines),
        "warning_count": len(warning_lines),
        "first_error": error_lines[0] if error_lines else None,
    }

    return result