"""
gui.py
------
Graphical User Interface (GUI) wrapper for the Python Log Analyzer.
Built using standard Tkinter and modern ttk widgets, providing a complete
resume-worthy dashboard experience.
"""

import os
import sys
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

# Import Pillow (PIL) for robust cross-platform image viewing in Tkinter.
# Improve GUI chart rendering compatibility by replacing tk.PhotoImage with Pillow.
try:
    from PIL import Image, ImageTk
    PILLOW_AVAILABLE = True
except ImportError:
    # If Pillow is not installed, we fallback to standard Tkinter's native PNG capability.
    PILLOW_AVAILABLE = False

# Import core parsing engine
import analyzer

class LogAnalyzerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Log Analyzer Dashboard")
        self.root.geometry("950x670")
        self.root.minsize(800, 580)
        
        # State variables
        self.current_filepath = "sample.log"
        self.parsed_logs = []
        self.invalid_count = 0
        self.filtered_logs = []
        
        # Configure overall grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(2, weight=1)  # Table row expands
        
        # Set up modern ttk styling
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Crisp, clean cross-platform theme
        
        # Customize Treeview and Button fonts and colors
        self.style.configure("TButton", font=("Segoe UI", 10), padding=5)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        self.style.configure("Treeview", font=("Segoe UI", 9), rowheight=24)
        
        # Create different layout frames
        self.create_top_file_frame()
        self.create_filter_frame()
        self.create_main_view_frame()
        self.create_bottom_action_frame()
        
        # Startup check in gui.py: If sample.log does not exist, automatically create it
        try:
            analyzer.ensure_sample_log_exists(self.current_filepath)
        except Exception as e:
            messagebox.showwarning("Startup Warning", f"Could not create default sample log: {e}")
        
        # Pre-load sample.log if it exists
        if os.path.exists(self.current_filepath):
            self.load_log_file(self.current_filepath)
        else:
            self.update_stats_display(None)

    def create_top_file_frame(self):
        """
        Creates the top control panel for browsing and loading log files.
        """
        top_frame = ttk.LabelFrame(self.root, text=" 📂 Log File Selector ", padding=10)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=15, pady=10)
        
        top_frame.columnconfigure(1, weight=1)
        
        ttk.Label(top_frame, text="File Path:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        
        self.path_entry_var = tk.StringVar(value=self.current_filepath)
        self.path_entry = ttk.Entry(top_frame, textvariable=self.path_entry_var, font=("Segoe UI", 10))
        self.path_entry.grid(row=0, column=1, padx=5, sticky="ew")
        
        browse_btn = ttk.Button(top_frame, text="Browse...", command=self.browse_file)
        browse_btn.grid(row=0, column=2, padx=5)
        
        load_btn = ttk.Button(top_frame, text="Parse File", command=self.on_load_clicked)
        load_btn.grid(row=0, column=3, padx=5)

    def create_filter_frame(self):
        """
        Creates the filtering, keyword search, and sorting controls.
        """
        filter_frame = ttk.LabelFrame(self.root, text=" 🔍 Filters & Queries ", padding=10)
        filter_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=15, pady=5)
        
        # Log level selection dropdown
        ttk.Label(filter_frame, text="Log Level:", font=("Segoe UI", 9, "bold")).grid(row=0, column=0, padx=5, sticky="w")
        self.level_var = tk.StringVar(value="ALL")
        levels = ["ALL"] + analyzer.VALID_LEVELS
        self.level_combo = ttk.Combobox(filter_frame, textvariable=self.level_var, values=levels, state="readonly", width=12)
        self.level_combo.grid(row=0, column=1, padx=5, sticky="w")
        
        # Keyword query string search
        ttk.Label(filter_frame, text="Keyword Search:", font=("Segoe UI", 9, "bold")).grid(row=0, column=2, padx=5, sticky="w")
        self.keyword_var = tk.StringVar()
        self.keyword_entry = ttk.Entry(filter_frame, textvariable=self.keyword_var, width=25)
        self.keyword_entry.grid(row=0, column=3, padx=5, sticky="w")
        
        # Chronological sorting checkbox
        self.sort_var = tk.BooleanVar(value=False)
        self.sort_check = ttk.Checkbutton(filter_frame, text="Sort by Timestamp", variable=self.sort_var)
        self.sort_check.grid(row=0, column=4, padx=15, sticky="w")
        
        # Filter action button
        apply_btn = ttk.Button(filter_frame, text="Apply Filter", command=self.apply_filters_and_update)
        apply_btn.grid(row=0, column=5, padx=10)

    def create_main_view_frame(self):
        """
        Creates the main screen showing a sidebar dashboard and a center scrollable Treeview.
        """
        # Outer container frame
        self.container_frame = ttk.Frame(self.root)
        self.container_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=15, pady=10)
        self.container_frame.columnconfigure(0, weight=3) # treeview
        self.container_frame.columnconfigure(1, weight=1) # stats panel
        self.container_frame.rowconfigure(0, weight=1)
        
        # Left side: Scrollable treeview
        tree_container = ttk.Frame(self.container_frame)
        tree_container.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        
        tree_container.columnconfigure(0, weight=1)
        tree_container.rowconfigure(0, weight=1)
        
        # Treeview setup
        columns = ("timestamp", "level", "message")
        self.tree = ttk.Treeview(tree_container, columns=columns, show="headings")
        self.tree.grid(row=0, column=0, sticky="nsew")
        
        # Define table headings
        self.tree.heading("timestamp", text="Timestamp", anchor="w")
        self.tree.heading("level", text="Level", anchor="w")
        self.tree.heading("message", text="Log Message Details", anchor="w")
        
        # Set column widths
        self.tree.column("timestamp", width=160, minwidth=140, stretch=False)
        self.tree.column("level", width=90, minwidth=80, stretch=False)
        self.tree.column("message", width=350, minwidth=200, stretch=True)
        
        # Add scrollbars
        scrollbar_y = ttk.Scrollbar(tree_container, orient="vertical", command=self.tree.yview)
        scrollbar_y.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar_y.set)
        
        # Right side: Statistics Dashboard Panel
        self.create_stats_dashboard()

    def create_stats_dashboard(self):
        """
        Builds the statistics visualization panel on the right sidebar.
        """
        self.stats_frame = ttk.LabelFrame(self.container_frame, text=" 📊 Statistics Dashboard ", padding=10)
        self.stats_frame.grid(row=0, column=1, sticky="nsew")
        
        # Layout weights
        for i in range(10):
            self.stats_frame.rowconfigure(i, weight=1)
        self.stats_frame.columnconfigure(0, weight=1)
        
        # Widgets for counts
        self.total_lbl = ttk.Label(self.stats_frame, text="Total Lines: -", font=("Segoe UI", 10, "bold"))
        self.total_lbl.grid(row=0, column=0, sticky="w", pady=2)
        
        self.valid_lbl = ttk.Label(self.stats_frame, text="Valid Logs: -", font=("Segoe UI", 10, "bold"), foreground="green")
        self.valid_lbl.grid(row=1, column=0, sticky="w", pady=2)
        
        self.invalid_lbl = ttk.Label(self.stats_frame, text="Invalid Skipped: -", font=("Segoe UI", 10, "bold"), foreground="red")
        self.invalid_lbl.grid(row=2, column=0, sticky="w", pady=2)
        
        # Separator line
        sep = ttk.Separator(self.stats_frame, orient="horizontal")
        sep.grid(row=3, column=0, sticky="ew", pady=5)
        
        # Individual level headers
        ttk.Label(self.stats_frame, text="Level Breakdown:", font=("Segoe UI", 9, "underline")).grid(row=4, column=0, sticky="w", pady=2)
        
        self.level_labels = {}
        row_idx = 5
        for level in analyzer.VALID_LEVELS:
            lbl = ttk.Label(self.stats_frame, text=f"• {level}: -", font=("Segoe UI", 9, "bold"))
            lbl.grid(row=row_idx, column=0, sticky="w", pady=1)
            self.level_labels[level] = lbl
            row_idx += 1

    def create_bottom_action_frame(self):
        """
        Creates the bottom frame holding action buttons (exports, visualization, exits).
        """
        bottom_frame = ttk.Frame(self.root, padding=10)
        bottom_frame.grid(row=3, column=0, columnspan=2, sticky="ew", padx=15, pady=5)
        
        # Arrange layout columns
        bottom_frame.columnconfigure(0, weight=1)
        
        button_container = ttk.Frame(bottom_frame)
        button_container.grid(row=0, column=0, sticky="e")
        
        export_txt_btn = ttk.Button(button_container, text="Export TXT Report", command=self.export_txt)
        export_txt_btn.grid(row=0, column=0, padx=5)
        
        export_csv_btn = ttk.Button(button_container, text="Export CSV Logs", command=self.export_csv)
        export_csv_btn.grid(row=0, column=1, padx=5)
        
        chart_btn = ttk.Button(button_container, text="View Level Chart", command=self.show_chart_modal)
        chart_btn.grid(row=0, column=2, padx=5)
        
        exit_btn = ttk.Button(button_container, text="Close Dashboard", command=self.root.destroy)
        exit_btn.grid(row=0, column=3, padx=5)

    def browse_file(self):
        """
        Opens a standard Windows File Dialog to select log files.
        """
        filepath = filedialog.askopenfilename(
            initialdir=".",
            title="Select Log File",
            filetypes=(("Log files", "*.log"), ("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filepath:
            self.path_entry_var.set(filepath)
            self.load_log_file(filepath)

    def on_load_clicked(self):
        """
        Fires when the manual 'Parse File' button is clicked.
        """
        filepath = self.path_entry_var.get().strip()
        if not filepath:
            messagebox.showerror("Error", "Please provide a valid file path.")
            return
        self.load_log_file(filepath)

    def load_log_file(self, filepath):
        """
        EXCEPTION HANDLING IN GUI:
        Loads and parses the log file, trapping filesystem errors (file missing, directory choice,
        permission restrictions) and reporting friendly error diagnostics in popup windows instead of crashing.
        """
        try:
            logs, invalid = analyzer.read_log_file(filepath)
            
            # Save parsed states
            self.current_filepath = filepath
            self.parsed_logs = logs
            self.invalid_count = invalid
            
            # Apply any filters currently selected in GUI fields
            self.apply_filters_and_update()
            
            messagebox.showinfo("Success", f"Log file loaded successfully!\nParsed {len(logs)} valid lines.\nSkipped {invalid} invalid lines.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"File '{filepath}' not found.\nPlease make sure the path is correct.")
            self.update_stats_display(None)
        except PermissionError:
            messagebox.showerror("Error", f"Permission denied while reading '{filepath}'.\nPlease check directory privileges.")
            self.update_stats_display(None)
        except IsADirectoryError:
            messagebox.showerror("Error", f"Path '{filepath}' is a directory, not a file.\nPlease specify a direct log file.")
            self.update_stats_display(None)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load file:\n{str(e)}")
            self.update_stats_display(None)

    def apply_filters_and_update(self):
        """
        Filters and sorts logs in accordance with the GUI options, and updates visual tables and stats.
        """
        if not self.parsed_logs and self.invalid_count == 0:
            self.clear_table()
            return
            
        selected_level = self.level_var.get()
        level_filter = None if selected_level == "ALL" else selected_level
        keyword_filter = self.keyword_var.get().strip()
        keyword_filter = None if not keyword_filter else keyword_filter
        sort_by_time = self.sort_var.get()
        
        # Run filter
        self.filtered_logs = analyzer.filter_logs(
            self.parsed_logs, 
            level=level_filter, 
            keyword=keyword_filter, 
            sort_by_timestamp=sort_by_time
        )
        
        # Update Table view
        self.populate_table(self.filtered_logs)
        
        # Recalculate statistics based on the active log view
        stats = analyzer.calculate_statistics(self.parsed_logs, self.invalid_count)
        self.update_stats_display(stats)

    def clear_table(self):
        """
        Clears all items in the log viewer Treeview.
        """
        for item in self.tree.get_children():
            self.tree.delete(item)

    def populate_table(self, logs):
        """
        TREEVIEW POPULATION EXPLANATION:
        1. We clear any existing rows currently in the Treeview grid to prepare a fresh display.
        2. We loop through the filtered log items.
        3. For each dictionary, we insert the capture groups (Timestamp, Level, Message) as columns.
        4. Modern tree components handle massive logs smoothly with lazy scroll rendering.
        """
        self.clear_table()
        for log in logs:
            self.tree.insert("", "end", values=(log["timestamp"], log["level"], log["message"]))

    def update_stats_display(self, stats):
        """
        Redraws statistics figures in the dashboard.
        """
        if stats is None:
            self.total_lbl.config(text="Total Lines: -")
            self.valid_lbl.config(text="Valid Logs: -")
            self.invalid_lbl.config(text="Invalid Skipped: -")
            for level, lbl in self.level_labels.items():
                lbl.config(text=f"• {level}: -")
            return
            
        self.total_lbl.config(text=f"Total Lines: {stats['total_entries']}")
        self.valid_lbl.config(text=f"Valid Logs: {stats['total_valid']}")
        self.invalid_lbl.config(text=f"Invalid Skipped: {stats['invalid_skipped']}")
        
        for level, count in stats["level_counts"].items():
            if level in self.level_labels:
                self.level_labels[level].config(text=f"• {level}: {count}")

    def export_txt(self):
        """
        Saves a text report of the CURRENT FILTERED dataset using standard File Dialogs.
        """
        if not self.parsed_logs:
            messagebox.showwarning("Warning", "No parsed log data is currently loaded to export.")
            return
            
        save_path = filedialog.asksaveasfilename(
            initialfile="report.txt",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if save_path:
            try:
                # Recalculate stats dynamically for the active filtered segment
                active_invalid = 0 if len(self.filtered_logs) < len(self.parsed_logs) else self.invalid_count
                stats = analyzer.calculate_statistics(self.filtered_logs, active_invalid)
                analyzer.generate_txt_report(stats, self.filtered_logs, save_path)
                messagebox.showinfo("Export Success", f"TXT report successfully saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Could not export report:\n{e}")

    def export_csv(self):
        """
        Saves a CSV log file of the CURRENT FILTERED dataset using standard File Dialogs.
        """
        if not self.filtered_logs:
            messagebox.showwarning("Warning", "No log records exist in the current filtered segment to export.")
            return
            
        save_path = filedialog.asksaveasfilename(
            initialfile="report.csv",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if save_path:
            try:
                analyzer.generate_csv_report(self.filtered_logs, save_path)
                messagebox.showinfo("Export Success", f"CSV file successfully saved to:\n{save_path}")
            except Exception as e:
                messagebox.showerror("Export Failed", f"Could not export logs to CSV:\n{e}")

    def show_chart_modal(self):
        """
        VISUALIZATION GENERATION IN GUI & COMPATIBLE PILLOW RENDERER:
        1. Compiles counts and saves a distribution plot using 'matplotlib' as 'report_chart.png'.
        2. Spawns a separate modal window ('tk.Toplevel') to view the graph.
        3. If Pillow is available, it opens the PNG file via 'PIL.Image.open()' and converts
           it to a Tkinter-compatible 'ImageTk.PhotoImage' format. This provides high stability
           across various python environments.
        4. If Pillow is unavailable, it gracefully falls back to using Tkinter's native
           'tk.PhotoImage()'. In modern Tkinter, native PhotoImage handles PNGs without Pillow.
        5. If both image readers fail, it catches the error and informs the user that the chart
           was exported successfully to 'report_chart.png' and is available for manual opening.
        """
        if not self.parsed_logs:
            messagebox.showwarning("Warning", "No logs loaded. Please parse a log file first.")
            return
            
        png_chart_path = "report_chart.png"
        
        # Calculate active statistics (based on the currently filtered log view)
        active_invalid = 0 if len(self.filtered_logs) < len(self.parsed_logs) else self.invalid_count
        stats = analyzer.calculate_statistics(self.filtered_logs, active_invalid)
        
        # Try generating chart using the analyzer engine
        success = analyzer.generate_visualization(stats, png_chart_path)
        if not success:
            messagebox.showerror("Error", "Could not generate chart. Please make sure 'matplotlib' library is installed.\nRun 'pip install -r requirements.txt'")
            return
            
        # Display image in a new window modal
        chart_window = tk.Toplevel(self.root)
        chart_window.title("Log Level Distribution Chart")
        chart_window.geometry("820x520")
        chart_window.resizable(False, False)
        chart_window.grab_set() # Focus lock
        
        img_label = None
        
        # Attempt Pillow loader first
        if PILLOW_AVAILABLE:
            try:
                pil_img = Image.open(png_chart_path)
                tk_img = ImageTk.PhotoImage(pil_img)
                img_label = ttk.Label(chart_window, image=tk_img)
                img_label.image = tk_img  # Store reference
                img_label.pack(fill="both", expand=True, padx=10, pady=10)
            except Exception as e:
                # Fallback to native loader if Pillow fails
                print(f"Pillow loader warning: {e}. Falling back to native loader.")
                
        # Graceful fallback to native PhotoImage if Pillow is absent or failed
        if img_label is None:
            try:
                native_img = tk.PhotoImage(file=png_chart_path)
                img_label = ttk.Label(chart_window, image=native_img)
                img_label.image = native_img  # Store reference
                img_label.pack(fill="both", expand=True, padx=10, pady=10)
            except Exception as e:
                # If both loader systems fail, display description warning
                chart_window.destroy()
                messagebox.showinfo("Chart Exported", f"Chart successfully generated and saved to disk:\n{os.path.abspath(png_chart_path)}\n\n(Cannot render inline inside window: {e})")
                return
                
        # Inform user
        messagebox.showinfo("Chart Refreshed", f"Distribution chart generated from currently filtered records and saved as:\n{os.path.abspath(png_chart_path)}")

if __name__ == "__main__":
    root_window = tk.Tk()
    app = LogAnalyzerGUI(root_window)
    root_window.mainloop()