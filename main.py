"""
main.py
-------
Main interactive Command-Line Interface (CLI) for the Python Log Analyzer.
Integrates colorama terminal colors, file loaders, filter search, report exports,
matplotlib visualizer, and a real-time monitor loop.
"""

import os
import sys
import time
import subprocess
from colorama import init, Fore, Style

# Import our helper functions and constants from analyzer.py
import analyzer

# Initialize colorama and auto-reset colors after each print statement
init(autoreset=True)

def print_banner():
    """
    Displays a premium, highly compatible ASCII banner for the Python Log Analyzer.
    Uses standard character sets to render flawlessly in Windows terminals.
    """
    banner = f"""
{Fore.CYAN}  ┌──────────────────────────────────────────────────────────────┐
{Fore.GREEN}   __    ____  ____    ____  _  _   __   __   _  _  ____  ____ 
{Fore.GREEN}  (  )  (  _ \( ___)  (  _ \( \/ ) /__\ (  ) ( \/ )(  _ \(  _ \\
{Fore.GREEN}   )(__  )   / )__)    ) _ ( \  / /(__)\ )(__  \  /  )   / )   /
{Fore.GREEN}  (____)(_)\_)(____)  (____/  \/ (_)(_)(____)  \/  (_)\_)(_)\_)
{Fore.YELLOW}  ==============================================================
{Fore.YELLOW}                   LOG DIAGNOSTICS CONTROL v1.0
{Fore.CYAN}  └──────────────────────────────────────────────────────────────┘
    """
    print(banner)

def get_color_for_level(level):
    """
    Returns the appropriate Colorama foreground color for a given log level.
    
    Args:
        level (str): The log level (e.g., 'INFO', 'ERROR').
        
    Returns:
        str: Colorama Fore color code.
    """
    level_colors = {
        "INFO": Fore.GREEN,
        "WARNING": Fore.YELLOW,
        "ERROR": Fore.RED,
        "DEBUG": Fore.CYAN,
        "CRITICAL": Fore.MAGENTA
    }
    return level_colors.get(level.upper(), Fore.WHITE)

def print_stats(stats, title="SUMMARY STATISTICS"):
    """
    Prints a formatted summary of log statistics in corresponding log-level colors.
    """
    print(f"\n{Fore.BLUE}{Style.BRIGHT}==========================================")
    print(f"{Fore.BLUE}{Style.BRIGHT}           {title}")
    print(f"{Fore.BLUE}{Style.BRIGHT}==========================================")
    print(f"Total Log Entries Processed : {stats['total_entries']}")
    print(f"Valid Log Entries Found     : {Fore.GREEN}{stats['total_valid']}")
    print(f"Invalid Lines Skipped       : {Fore.RED if stats['invalid_skipped'] > 0 else Fore.WHITE}{stats['invalid_skipped']}")
    print(f"------------------------------------------")
    print("LOG LEVEL BREAKDOWN:")
    
    for level, count in stats["level_counts"].items():
        color = get_color_for_level(level)
        print(f"  - {color}{level:<10}{Style.RESET_ALL}: {count}")
    print(f"{Fore.BLUE}{Style.BRIGHT}==========================================\n")

def display_logs(logs):
    """
    Displays a list of logs in a clean, colored tabular format.
    """
    if not logs:
        print(f"\n{Fore.YELLOW}No matching log entries found.")
        return

    # Print table header
    header = f"{'TIMESTAMP':<20} | {'LEVEL':<8} | {'MESSAGE'}"
    print(f"\n{Style.BRIGHT}{header}")
    print("-" * 80)
    
    # Print each line in its level color
    for log in logs:
        color = get_color_for_level(log["level"])
        print(f"{color}{log['timestamp']:<20} | {log['level']:<8} | {log['message']}")
    print("-" * 80)
    print(f"Showing {len(logs)} log entries.\n")

def load_log_file_interactive():
    """
    Asks the user for a log file path with input validation and loop retry on error.
    
    Returns:
        tuple: (list of parsed logs, int count of invalid lines, str verified path)
    """
    while True:
        try:
            print_banner()
            default_path = "sample.log"
            
            # STARTUP CHECK: If default sample.log doesn't exist, create it automatically
            analyzer.ensure_sample_log_exists(default_path)
            
            prompt = f"Enter log file path (Press Enter for '{Fore.GREEN}{default_path}{Fore.WHITE}'): "
            path_input = input(prompt).strip()
            
            # Use default path if user presses Enter
            file_path = path_input if path_input else default_path
            
            # Verify path and read using our analyzer library
            print(f"\n{Fore.CYAN}Loading and parsing '{file_path}'...")
            logs, invalid_count = analyzer.read_log_file(file_path)
            
            print(f"{Fore.GREEN}✓ File successfully loaded and parsed!")
            return logs, invalid_count, file_path
            
        # EXCEPTION HANDLING: Trap common filesystem errors and display meaningful descriptions
        except FileNotFoundError as e:
            print(f"\n{Fore.RED}ERROR: The file does not exist. Please check the path and try again.")
            print(f"{Fore.RED}System Detail: {e}\n")
        except PermissionError as e:
            print(f"\n{Fore.RED}ERROR: Permission denied. You do not have permissions to read this file.")
            print(f"{Fore.RED}System Detail: {e}\n")
        except IsADirectoryError as e:
            print(f"\n{Fore.RED}ERROR: The specified path is a directory, not a file.")
            print(f"{Fore.RED}System Detail: {e}\n")
        except Exception as e:
            print(f"\n{Fore.RED}ERROR: An unexpected error occurred while reading the file.")
            print(f"{Fore.RED}System Detail: {e}\n")
            
        # Give option to exit if they are stuck
        retry = input("Would you like to try again? (y/n): ").strip().lower()
        if retry != 'y' and retry != 'yes':
            print(f"\n{Fore.YELLOW}Exiting Log Analyzer. Goodbye!")
            sys.exit(0)

def run_realtime_monitor(file_path):
    """
    REAL-TIME MONITORING EXPLANATION:
    Implements a polling mechanism similar to Unix's 'tail -f'.
    1. We open the file and jump directly to the end using 'file.seek(0, os.SEEK_END)'.
    2. We enter an infinite loop checking for new file additions.
    3. If new data is written to the file, 'file.readline()' catches it immediately,
       parses it using our regex parser, and outputs it in color-coded lines.
    4. If no data is written, 'readline()' returns an empty string. We sleep for
       0.5 seconds to prevent using 100% CPU capacity.
    5. We wrap this polling loop inside a 'try-except KeyboardInterrupt' block so that
       the user can safely press Ctrl+C to stop the monitor and return to the main CLI menu.
    """
    print(f"\n{Fore.MAGENTA}{Style.BRIGHT}======================================================================")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}         STARTING REAL-TIME LOG MONITOR ({file_path})")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}         Press Ctrl+C to return to main menu.")
    print(f"{Fore.MAGENTA}{Style.BRIGHT}======================================================================")
    
    try:
        # Open file and seek to the end of it
        with open(file_path, "r", encoding="utf-8") as file:
            file.seek(0, os.SEEK_END)
            print(f"{Fore.CYAN}Waiting for new log events...")
            
            while True:
                line = file.readline()
                if not line:
                    # No new line found, pause briefly and check again
                    time.sleep(0.5)
                    continue
                
                # We found a new line! Parse and print it
                parsed = analyzer.parse_log_line(line)
                if parsed:
                    color = get_color_for_level(parsed["level"])
                    print(f"{color}[LIVE] {parsed['timestamp']} [{parsed['level']}] {parsed['message']}")
                else:
                    # Skip empty newlines but warn about malformed/invalid appends
                    if line.strip():
                        print(f"{Fore.RED}[LIVE][MALFORMED LOG SKIPPED] {line.strip()}")
                        
    except KeyboardInterrupt:
        print(f"\n\n{Fore.GREEN}Real-time monitor stopped. Returning to main menu.\n")
    except Exception as e:
        print(f"\n{Fore.RED}ERROR: Real-time monitor encountered a failure: {e}\n")

def main():
    """
    Main execution loop driving the interactive CLI.
    """
    # Load default logs and statistics
    logs, invalid_count, current_path = load_log_file_interactive()
    
    # Track the active dataset which might be filtered by search conditions
    active_logs = list(logs)
    active_invalid = invalid_count
    is_filtered = False
    
    while True:
        # Calculate statistics dynamically based on the current active log view
        stats = analyzer.calculate_statistics(active_logs, active_invalid)
        
        # Display the current file path and record size
        status_label = f"FILTERS ACTIVE (N={len(active_logs)})" if is_filtered else "ALL LOGS ACTIVE"
        print(f"\n{Fore.CYAN}{Style.BRIGHT}>>> FILE: {Fore.YELLOW}{current_path}{Fore.CYAN} | {Fore.GREEN}{status_label}{Fore.CYAN} | TOTAL VISIBLE: {Fore.YELLOW}{stats['total_entries']}")
        
        print(f"{Fore.BLUE}------------------------------------------")
        print("INTERACTIVE OPTIONS:")
        print("  1. Display Summary Statistics")
        print("  2. Search & Filter Log Entries")
        print("  3. Export Filtered Logs (TXT & CSV)")
        print("  4. Generate Log Level Visualizations (Matplotlib)")
        print("  5. Start Real-time Log Monitoring (tail -f)")
        print("  6. Launch Graphical Interface (Tkinter GUI)")
        print("  7. Load a Different Log File / Reset Filters")
        print("  8. Exit Program")
        print(f"{Fore.BLUE}------------------------------------------")
        
        choice = input("Select an option (1-8): ").strip()
        
        if choice == "1":
            title = "FILTERED SUMMARY STATISTICS" if is_filtered else "SUMMARY STATISTICS"
            print_stats(stats, title)
            
        elif choice == "2":
            print(f"\n{Fore.CYAN}--- SEARCH & FILTER LOGS ---")
            
            # 1. Level filter
            print(f"Available levels: {', '.join(analyzer.VALID_LEVELS)}")
            lvl_input = input("Enter log level to filter (Press Enter for ALL): ").strip().upper()
            level = lvl_input if lvl_input in analyzer.VALID_LEVELS else None
            
            # 2. Keyword filter
            keyword = input("Enter search keyword query (Press Enter for NONE): ").strip()
            keyword = keyword if keyword else None
            
            # 3. Optional sorting
            sort_input = input("Sort logs chronologically by timestamp? (y/n, Default: n): ").strip().lower()
            sort_by_time = sort_input in ["y", "yes"]
            
            # Perform filter and sorting from the full set of logs
            active_logs = analyzer.filter_logs(logs, level=level, keyword=keyword, sort_by_timestamp=sort_by_time)
            
            # If filters are active, we set skipped lines count to 0 in the stats display
            # because malformed lines do not belong to filtered queries.
            if level or keyword:
                active_invalid = 0
                is_filtered = True
            else:
                active_invalid = invalid_count
                is_filtered = False
                
            display_logs(active_logs)
            
        elif choice == "3":
            # Dynamic CLI Export functionality:
            # If the user has applied filters, the exported files contain ONLY the active filtered records
            # and statistics are recalculated specifically for this subset.
            export_type = "Filtered Log Segment" if is_filtered else "Full Log File"
            print(f"\n{Fore.CYAN}--- EXPORTING REPORTS ({export_type}) ---")
            
            txt_path = "report.txt"
            csv_path = "report.csv"
            
            try:
                # Export using the active logs list and its statistics
                analyzer.generate_txt_report(stats, active_logs, txt_path)
                analyzer.generate_csv_report(active_logs, csv_path)
                
                print(f"{Fore.GREEN}✓ Text report successfully exported to: {Fore.YELLOW}{os.path.abspath(txt_path)}")
                print(f"{Fore.GREEN}✓ CSV logs successfully exported to: {Fore.YELLOW}{os.path.abspath(csv_path)}")
            except Exception as e:
                print(f"{Fore.RED}ERROR: Export failed: {e}")
                
        elif choice == "4":
            print(f"\n{Fore.CYAN}--- GENERATING LOG DISTRIBUTION CHART ---")
            png_path = "report_chart.png"
            
            # Generate the visualization based on the currently displayed statistics
            success = analyzer.generate_visualization(stats, png_path)
            if success:
                print(f"{Fore.GREEN}✓ Chart successfully generated and saved to: {Fore.YELLOW}{os.path.abspath(png_path)}")
                print(f"{Fore.GREEN}Tip: Open this image file to see a premium distribution visual!")
            else:
                print(f"{Fore.YELLOW}Notice: Could not generate visualization chart.")
                print(f"{Fore.YELLOW}Reason: Either 'matplotlib' is not installed or there are no log statistics to display.")
                print(f"{Fore.YELLOW}Please ensure you ran 'pip install -r requirements.txt' successfully.")
                
        elif choice == "5":
            run_realtime_monitor(current_path)
            
        elif choice == "6":
            print(f"\n{Fore.CYAN}--- LAUNCHING TKINTER GUI SUBPROCESS ---")
            gui_file = "gui.py"
            if os.path.exists(gui_file):
                print(f"{Fore.GREEN}Starting GUI in background process... View the window on your taskbar!")
                # Launch GUI as an independent background process using the current Python executable
                subprocess.Popen([sys.executable, gui_file])
            else:
                print(f"{Fore.RED}ERROR: GUI script '{gui_file}' was not found in the directory.")
                
        elif choice == "7":
            # Reload file and reset all active filter states back to default
            logs, invalid_count, current_path = load_log_file_interactive()
            active_logs = list(logs)
            active_invalid = invalid_count
            is_filtered = False
            print(f"\n{Fore.GREEN}✓ Filters reset. Loaded all logs successfully.")
            
        elif choice == "8":
            print(f"\n{Fore.GREEN}Thank you for using the Python Log Analyzer! Goodbye.\n")
            sys.exit(0)
            
        else:
            print(f"\n{Fore.RED}Invalid input. Please enter a number between 1 and 8.")
            
        # Add a brief pause to allow the user to read outputs before redrawing menu
        input(f"\n{Fore.WHITE}Press Enter to return to options...")

if __name__ == "__main__":
    main()