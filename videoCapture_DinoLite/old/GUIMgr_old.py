import tkinter as tk
from threading import Thread, Event
import time
# Function to handle the start button click
UI_WIDTH = 500


class MySmallGUI:
    def __init__(self, onSTART, onPAUSE):
        # Create the main window
        self.root = tk.Tk()
        self.root.title("hii")

        # Bind the close event to the on_close function
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)


        # Create and place the Start button
        def flip_btn(callbackFUNCstart,callbackFUNCstop):
            if self.start_button['text'] == 'Start':
                callbackFUNCstart()
                self.start_button.config(text='Stop')
            else:
                callbackFUNCstop()
                self.start_button.config(text='Start')


        # Create a frame to organize the button and the first message label
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(pady=10, padx=10, anchor='w')
        
        # Create and place the button at the top-left side with fixed width
        self.start_button = tk.Button(self.top_frame, text="Start", width=10, command=lambda: flip_btn(onSTART,onPAUSE))
        self.start_button.pack(side=tk.LEFT)
        
        # Create and place the first message label to the right of the button
        self.title_label = tk.Label(self.top_frame, text="Title", font=("Helvetica", 16))
        self.title_label.pack(side=tk.LEFT, padx=10)
        
        # Create and place the second message label below the first message with a smaller font size
        self.subtitle_label = tk.Label(self.root, text="Subtitle", font=("Helvetica", 10))
        self.subtitle_label.pack(pady=10, anchor='w', padx=10)

        # bottom frame
        self.bottom_left_frame = tk.Frame(self.root, width=self.root.winfo_width()/4)
        self.bottom_left_frame.pack(pady=10, padx=10, anchor='w')
        # Create second input text box
        self.label1 = tk.Label(self.bottom_left_frame, text="Minigantry Delay")
        self.label1.pack(pady=5)
        self.entry1 = tk.Entry(self.bottom_left_frame)
        self.entry1.insert(tk.END, str(2))
        self.entry1.pack(pady=5)
        # bottom frame
        self.bottom_right_frame = tk.Frame(self.root, width=self.root.winfo_width()/4)
        self.bottom_right_frame.pack(pady=10, padx=10, anchor='w')
        # Create second input text box
        self.label2 = tk.Label(self.bottom_right_frame, text="Capturing Delay")
        self.label2.pack(pady=5)
        self.entry2 = tk.Entry(self.bottom_right_frame)
        self.entry2.insert(tk.END, str(1))
        self.entry2.pack(pady=5)


    def SetStatus(self,mesg):
        try:
            self.title_label.config(text=mesg)
        except: # not to raise error while showing message
            pass
    def SetAction(self,mesg):
        try:
            self.subtitle_label.config(text=mesg)
        except: # not to raise error while showing message
            pass


    def run(self):
        # Run the application
        self.root.mainloop()

# Function to handle the window close event
    def on_close(self):
        self.root.destroy()




# Example usage with dummy background job
if __name__ == "__main__":
    from bkg_process import ProgramStatus, bkg_run_job
    ps = ProgramStatus(3)

    def on_start():
        global ps
        ps.activatingFlag.set()

    def on_pause():
        global ps
        ps.activatingFlag.clear()

    def clear_job():
        global ps
        ps.programIsAlive.clear()


    # Create and run the GUI
    myGUI = MySmallGUI(on_start,on_pause)

    # run bkg job
    bkg_thread = bkg_run_job(ps, myGUI.SetStatus, myGUI.SetAction)
    
    # activate GUI as bkg job controller
    myGUI.run()

    # clear background job after close mark clicked
    clear_job()

