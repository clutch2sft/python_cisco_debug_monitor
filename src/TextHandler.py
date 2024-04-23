import logging
import tkinter as tk

class TextHandler(logging.Handler):
    def __init__(self, text_widget, max_lines=1000):
        super().__init__()
        self.text_widget = text_widget
        self.max_lines = max_lines  # Maximum lines to keep in the text widget

    def emit(self, record):
        # Safely update the widget with the new log record
        self.text_widget.after(0, self.do_emit, record)

    def do_emit(self, record):
        msg = self.format(record)
        if self.text_widget:
            self.text_widget.insert(tk.END, msg + '\n')
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
