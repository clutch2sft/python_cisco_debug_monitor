import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import threading
import sys
from pathlib import Path
from screeninfo import get_monitors

# Your existing path setup
current_dir = Path(__file__).parent
src_path = current_dir / 'src'
sys.path.append(str(src_path))

from gui_main import start_monitoring, stop_monitoring
from TextHandler import TextHandler

class AppGUI:
    def __init__(self, root):
        self.root = root
        root.title("Cisco Debug Monitor")
        self.initialize_gui()
        # Flag to indicate if the monitoring process is running
        self.monitoring_active = False
        
    def initialize_gui(self):
        # Ask user to choose a monitor
        monitor_info = "\n".join(f"{i}: {m.name} {m.width}x{m.height}+{m.x}+{m.y}" for i, m in enumerate(get_monitors()))
        # choice = simpledialog.askinteger("Choose Monitor", f"Enter the number of the monitor to use:\n{monitor_info}", minvalue=0, maxvalue=len(get_monitors()) - 1)
        # if choice is None:  # User closed the dialog or clicked cancel
        #     self.root.destroy()
        #     return
        selected_monitor = get_monitors()[0]

        # Set window size to 3/4 of the selected monitor size
        width = int(selected_monitor.width * 0.75)
        height = int(selected_monitor.height * 0.75)
        x = selected_monitor.x + (selected_monitor.width - width) // 2
        y = selected_monitor.y + (selected_monitor.height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

        # Add a label just for demonstration
        # label = tk.Label(self.root, text=f"App running on {selected_monitor.name}, {width}x{height} at position {x}, {y}")
        # label.pack(pady=20)


        # Configure grid layout
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Text widget for output
        self.output = scrolledtext.ScrolledText(root, height=10, width=100)
        self.output.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)

        # Frame for buttons
        button_frame = tk.Frame(root)
        button_frame.grid(row=2, column=0, sticky='ew')

        # Start and Stop buttons centered in the frame
        self.start_button = tk.Button(button_frame, text="Start", command=self.start_process)
        self.start_button.pack(side='left', padx=5, pady=5)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_process)
        self.stop_button.pack(side='left', padx=5, pady=5)

        # Quit button in the main window, under the frame
        self.quit_button = tk.Button(root, text="Quit", command=self.quit_application)
        self.quit_button.grid(row=3, column=0, pady=10)
        # Handling close button safely
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        if self.monitoring_active:
            if not hasattr(self, 'closing_confirmed') or not self.closing_confirmed:
                # Ask for confirmation only once
                if messagebox.askyesno("Quit", "A monitoring process is still running. Do you want to stop it and quit?"):
                    self.closing_confirmed = True
                    self.stop_process()
                else:
                    # User chose not to quit after all
                    return
            # After confirming, check periodically if it's safe to close
            if self.monitoring_active:
                self.root.after(100, self.on_close)  # Check again after some delay
            else:
                self.root.destroy()
        else:
            self.root.destroy()


    def start_process(self):
        if not self.monitoring_active:
            self.monitoring_active = True
            text_handler = TextHandler(self.output, max_lines=10000)
            self.monitor_thread = threading.Thread(target=start_monitoring, args=(text_handler,))
            self.monitor_thread.start()
            self.quit_button.config(state='disabled')  # Disable the Quit button

    def check_thread(self):
        if self.monitor_thread.is_alive():
            # If the thread is still running, check again after some time
            self.root.after(100, self.check_thread)  # Check every 100 ms
        else:
            # Once the thread is no longer alive, update the GUI
            self.monitoring_active = False
            self.quit_button.config(state='normal')  # Re-enable the Quit button


    def stop_process(self):
        if self.monitoring_active:
            stop_monitoring()  # Signal the monitoring to stop
            self.check_thread()  # Start periodic checks to see if the thread has stopped


    def quit_application(self):
        if self.monitoring_active:
            self.stop_process()  # Signal the monitoring to stop
            self.root.after(100, self.quit_application)  # Check again shortly if it's safe to quit
        else:
            self.root.destroy()  # Safe to destroy the root and close the application


if __name__ == "__main__":
    root = tk.Tk()
    app = AppGUI(root)
    root.mainloop()
