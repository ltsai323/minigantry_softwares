import tkinter as tk
from tkinter import messagebox
from frag_global_vars import ProgramStatus

# Function to handle the Run button click
def run_action():
    message_label.config(text="Running...")

# Function to handle the Stop button click
def stop_action():
    message_label.config(text="Stopped.")

if __name__ == "__main__":
# Create the main window
    root = tk.Tk()
    root.title("Command Post")

# Create and place the Run button
    run_button = tk.Button(root, text="Run", command=run_action)
    run_button.pack(pady=10)

# Create and place the Stop button
    pause_button = tk.Button(root, text="Stop", command=pause_action)
    pause_button.pack(pady=10)

# Create and place the Stop button
    stop_button = tk.Button(root, text="Stop", command=stop_action)
    stop_button.pack(pady=10)

# Create and place the message label
    message_label = tk.Label(root, text="Welcome!")
    message_label.pack(pady=10)

# Run the application
    root.mainloop()
