import logging
import tkinter as tk

class TextHandler(logging.Handler):
    def __init__(self, text_widget, max_lines=1000):
        super().__init__()
        self.text_widget = text_widget
        self.max_lines = max_lines  # Maximum lines to keep in the text widget
        self.setup_tags()

    def setup_tags(self):
        # Setting up tags for different log levels and specific messages
        self.text_widget.tag_config('DEBUG', foreground='gray')
        self.text_widget.tag_config('INFO', foreground='black')
        self.text_widget.tag_config('WARNING', foreground='orange')
        self.text_widget.tag_config('ERROR', foreground='red')
        self.text_widget.tag_config('CRITICAL', foreground='red', underline=1)
        # Specific message tags
        self.text_widget.tag_config('ROAM_SWITCH', foreground='red')
        self.text_widget.tag_config('ASSOCIATED_AP', foreground='green')

    def emit(self, record):
        # Safely update the widget with the new log record
        self.text_widget.after(0, self.do_emit, record)

    def do_emit(self, record):
        msg = self.format(record)
        if self.text_widget:
            # Select tag based on specific phrases or log level
            if "Aux roam switch radio role" in msg:
                tag = 'ROAM_SWITCH'
            elif "Associated To AP" in msg:
                tag = 'ASSOCIATED_AP'
            else:
                # Default to log level tag
                log_level = record.levelname
                tag = log_level if hasattr(self, log_level) else 'INFO'

            self.text_widget.insert(tk.END, msg + '\n', tag)
            self.text_widget.see(tk.END)  # Auto-scroll to the end
            self.trim_buffer()

    def trim_buffer(self):
        # Get all lines from the text widget
        lines = self.text_widget.get('1.0', tk.END).splitlines()

        # If the number of lines exceeds the maximum, trim them
        if len(lines) > self.max_lines:
            # Calculate how many lines to delete
            num_lines_over = len(lines) - self.max_lines
            # Delete the oldest lines that exceed the limit
            self.text_widget.delete('1.0', f'{num_lines_over + 1}.0')
