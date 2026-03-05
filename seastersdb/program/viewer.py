import tkinter as tk
from tkinter import scrolledtext, messagebox, Toplevel
from typing import Callable, List
from duckdb import ParserException, BinderException, CatalogException

__all__ = ["Viewer"]

def _extract_query(string: str, query_prefix: str) -> str:
    def remove_prefix(lines: List[str], prefix: str) -> str:
        return "\n".join([line[len(prefix):] for line in lines])
    
    lines = string.split("\n")
    i = 0
    char = lines[i][:len(query_prefix)]
    while char == query_prefix:
        i += 1
        char = lines[i][:len(query_prefix)]
    result = remove_prefix(lines[:i], query_prefix)

    return result

class Viewer:
    """
    Interactive viewer for a function that takes a string and returns a string.
    Displays the query, output, and error messages.
    """

    def __init__(self, query_func: Callable[[str], str], export_func: Callable[[str, str], None], title="Function Viewer"):
        self.qfunc = query_func
        self.efunc = export_func

        # Main window
        self.root = tk.Tk()
        self.root.title(title)

        # Query history
        self.history = []
        self.history_index = -1

        # Response history
        self.responses = []
        self.response_index = -1

        # Input frame
        self.input_label = tk.Label(self.root, text="Enter query:")
        self.input_label.pack(anchor="w")
        self.query_area = tk.Text(self.root, height=5, width=80)
        self.query_area.pack(fill="both", expand=True, padx=5, pady=5)
        self.query_area.bind("<Control-Return>", lambda e: self.run_query())
        self.query_area.bind("<Prior>", self.show_prev_history)
        self.query_area.bind("<Next>", self.show_next_history)

        # Send button
        self.send_button = tk.Button(self.root, text="Send", command=self.run_query)
        self.send_button.pack(pady=5)

        # Response frame
        self.response_label = tk.Label(self.root, text="Response:")
        self.response_label.pack(anchor="w")

        # Frame to hold text + vertical scrollbar
        frame = tk.Frame(self.root)
        frame.pack(fill="both", expand=True, padx=5, pady=2)

        self.response_area = tk.Text(frame, width=80, height=20, wrap="none")
        self.response_area.pack(side="left", fill="both", expand=True)
        self.response_area.configure(font=("Consolas", 10), state="disabled")

        vsb = tk.Scrollbar(frame, orient="vertical", command=self.response_area.yview)
        vsb.pack(side="right", fill="y")
        self.response_area.configure(yscrollcommand=vsb.set)

        # Horizontal scrollbar (below the text area)
        hsb = tk.Scrollbar(self.root, orient="horizontal", command=self.response_area.xview)
        hsb.pack(fill="x")
        self.response_area.configure(xscrollcommand=hsb.set)

        # Response history buttons
        lower_frame = tk.Frame(self.root)
        lower_frame.pack(anchor="w", pady=(2, 5))

        self.prev_button = tk.Button(lower_frame, text="<", command=self.show_prev_response)
        self.prev_button.pack(side="left")

        self.next_button = tk.Button(lower_frame, text=">", command=self.show_next_response)
        self.next_button.pack(side="left")

        # Export widgets on the right side of the same line
        export_frame = tk.Frame(lower_frame)
        export_frame.pack(side="right")

        # Entry with placeholder
        self.export_entry = tk.Entry(export_frame, width=30, fg="gray")
        self.export_entry.insert(0, "filename.csv")

        def on_focus_in(event):
            if self.export_entry.get() == "filename.csv":
                self.export_entry.delete(0, tk.END)
                self.export_entry.config(fg="black")

        def on_focus_out(event):
            if not self.export_entry.get():
                self.export_entry.insert(0, "filename.csv")
                self.export_entry.config(fg="gray")

        self.export_entry.bind("<FocusIn>", on_focus_in)
        self.export_entry.bind("<FocusOut>", on_focus_out)
        self.export_entry.pack(side="left", padx=5)

        # Export button
        self.export_button = tk.Button(export_frame, text="Export", command=self.export_response)
        self.export_button.pack(side="left")

        # Copy Button
        self.copy_button = tk.Button(lower_frame, text="Copy", command=self.copy_query)
        self.copy_button.pack(side="left", padx=5)

        # Status bar at bottom
        self.status_var = tk.StringVar()
        self.status_var.set("")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, anchor="w", relief="sunken")
        self.status_bar.pack(fill="x", side="bottom")


    def run_query(self):

        def prepend(string: str, prefix: str) -> str:
            return prefix + ("\n" + prefix).join(string.split("\n"))

        def to_ascii(string: str) -> str:
            def replace_list(string, old, new):
                if len(old) == 0:
                    return string
                else:
                    ch = old.pop()
                    return replace_list(string.replace(ch, new), old, new)
            
            lines = string.split("\n")
            hline = replace_list(lines[0], ["┌", "└", "┘", "┐", "├", "┬", "┴", "┤", "┼"], "+").replace("─", "-")
            result = "\n".join([line.replace("│", "|") if line and line[0] in {"│", " "} else (hline if line else "") for line in lines])
            return result.strip("\n")
        

        query = self.query_area.get("1.0", "end").strip()
        if query:
            self.history.append(query)
            self.history_index = len(self.history)
        else:
            return

        head = prepend(query, "> ")
        sep = "\n\n"

        try:
            result = self.qfunc(query)
            body = to_ascii(result)
        except (
            ParserException,
            BinderException,
            CatalogException,
        ) as e:
            body = f"Error: {e}"

        output = f"{head}{sep}{body}"

        self.responses.append(output)
        self.response_index = len(self.responses) - 1
        self._show_response(self.response_index)

        self.query_area.delete("1.0", "end")

    def _load_history_item(self):
        self.query_area.delete("1.0", "end")
        self.query_area.insert("1.0", self.history[self.history_index])
    
    def show_prev_history(self, event):
        if self.history and self.history_index > 0:
            self.history_index -= 1
            self._load_history_item()
        return "break"

    def show_next_history(self, event):
        if self.history and self.history_index < len(self.history) - 1:
            self.history_index += 1
            self._load_history_item()
        elif self.history_index == len(self.history) - 1:
            # move to blank buffer
            self.history_index = len(self.history)
            self.query_area.delete("1.0", "end")
        return "break"
    
    def _show_response(self, index):
        if 0 <= index < len(self.responses):
            self.response_area.config(state="normal")
            self.response_area.delete("1.0", "end")
            self.response_area.insert("1.0", self.responses[index])
            self.response_area.config(state="disabled")

    def show_prev_response(self):
        if self.response_index > 0:
            self.response_index -= 1
            self._show_response(self.response_index)

    def show_next_response(self):
        if self.response_index < len(self.responses) - 1:
            self.response_index += 1
            self._show_response(self.response_index)

    def _finish_export(self, filename):
        query = _extract_query(self.responses[self.response_index], "> ")

        try:
            self.efunc(filename, query)
            self.status_var.set(f"Exported to: {filename}")
        except Exception as e:
            self.status_var.set(f"Export failed: {e}")
        finally:
            self.export_button.config(state="normal")

        self.root.after(3000, lambda: self.status_var.set(""))
    
    def export_response(self):
        filename = self.export_entry.get().strip()

        if self.response_index == -1:
            self.status_var.set("No response to export.")
            self.root.after(3000, lambda: self.status_var.set(""))
            return

        if not filename or filename == "filename.csv":
            self.status_var.set("Please enter a valid filename.")
            self.root.after(3000, lambda: self.status_var.set(""))
            return

        # Disable export button
        self.export_button.config(state="disabled")
        self.status_var.set("Exporting...")

        # Run export in the event loop so UI stays responsive
        self.root.after(50, lambda: self._finish_export(filename))

    def copy_query(self):
        if self.response_index == -1:
            self.status_var.set("No query to copy.")
            self.root.after(3000, lambda: self.status_var.set(""))
            return

        query = _extract_query(self.responses[self.response_index], "> ")

        if query:
            self.root.clipboard_clear()  # Clear the current clipboard content
            self.root.clipboard_append(query)  # Append the query text to clipboard
            self.status_var.set("Query copied to clipboard.")  # Update status
        else:
            self.status_var.set("No query to copy.")  # Show a message if no query exists

        self.root.after(3000, lambda: self.status_var.set(""))

    def run(self):
        self.root.mainloop()
