#!/usr/bin/env python3
import tkinter as tk
from threading import Thread
import time

def create_gui(on_start, on_pause, on_stop, check_job_message):
    # Function to handle the start button click
    def start_action():
        on_start()
        message_label.config(text="Running...")

    # Function to handle the pause button click
    def pause_action():
        on_pause()
        message_label.config(text="Paused.")

    # Function to handle the stop button click
    def stop_action():
        on_stop()
        message_label.config(text="Stopped.")

    # Function to periodically check for job messages
    def check_for_updates():
        new_title, new_subtitle = check_job_message()
        if new_title:
            title_label.config(text=new_title)
        if new_subtitle:
            subtitle_label.config(text=new_subtitle)
        root.after(1000, check_for_updates)  # Check every 1000 milliseconds (1 second)

    # Create the main window
    root = tk.Tk()
    root.title("Start/Pause/Stop GUI")

    # Create and place the title label
    title_label = tk.Label(root, text="Title", font=("Helvetica", 16))
    title_label.pack(pady=10)

    # Create and place the subtitle label
    subtitle_label = tk.Label(root, text="Subtitle", font=("Helvetica", 12))
    subtitle_label.pack(pady=10)

    # Create a frame to hold the buttons
    button_frame = tk.Frame(root)
    button_frame.pack(pady=10)

    # Create and place the Start button
    start_button = tk.Button(button_frame, text="Start", command=start_action)
    start_button.pack(side=tk.LEFT, padx=10)

    # Create and place the Pause button
    pause_button = tk.Button(button_frame, text="Pause", command=pause_action)
    pause_button.pack(side=tk.LEFT, padx=10)

    # Create and place the Stop button
    stop_button = tk.Button(button_frame, text="Stop", command=stop_action)
    stop_button.pack(side=tk.LEFT, padx=10)

    # Create and place the message label
    message_label = tk.Label(root, text="Welcome!")
    message_label.pack(pady=10)

    # Start the periodic update check
    check_for_updates()

    # Run the application
    root.mainloop()

# Example usage with dummy background job
if __name__ == "__main__":
    # Callback functions
    def on_start():
        print("Started")

    def on_pause():
        print("Paused")

    def on_stop():
        print("Stopped")

    # Function to simulate background job messages
    def check_job_message():
        # Simulate changing messages
        current_time = time.strftime("%H:%M:%S")
        return f"Title at {current_time}", f"Subtitle at {current_time}"

    # Create and run the GUI
    create_gui(on_start, on_pause, on_stop, check_job_message)
