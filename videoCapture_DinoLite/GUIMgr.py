import tkinter as tk

def Status(mesg):
    print(f'[Status] {mesg}')
def Action(mesg):
    print(f'[Action] {mesg}')

debug_mode = False
class CustomGUI:
    def __init__(self, root, guiCONFITUABLE):
        self.root = root
        title = 'This is Title'
        subtitle = 'This is subtitle'
        self.root.title('Mini Gantry Photo Capturing Automator')
        self.root.geometry('400x250')
        self.root.attributes('-topmost', True)
        primary_font = ("Helvetica", 18)
        secondary_font = ("Helvetica", 10)
        timer_font = ("Helvetica", 10)

        # Store the button command function
        self.button_command = guiCONFITUABLE.setFUNC

        # Create title label
        self.title_label = tk.Label(root, text=title, font=primary_font, justify=tk.CENTER, anchor='c')
        self.title_label.pack(pady=10)

        # Create subtitle label
        self.subtitle_label = tk.Label(root, text=subtitle, font=secondary_font, justify=tk.LEFT, anchor='w')
        self.subtitle_label.pack(pady=5)

        # Dynamic input fields
        self.entries = {}
        self.create_dynamic_inputs(guiCONFITUABLE.configurations, timer_font)

        # Create the button
        self.set_button = tk.Button(root, text='Set Values', command=self.set_btn)
        self.set_button.pack(pady=10, side=tk.RIGHT)

        # remove this button
        ## Create and place the Start button
        #self.start_button = tk.Button(root, text='Start', command=lambda:self.flip_btn(guiCONFITUABLE.startFUNC, guiCONFITUABLE.pauseFUNC))
        #self.start_button.pack(pady=10, side=tk.RIGHT)
        if debug_mode:
            self.chk_button = tk.Button(root, text='check', command=lambda:print(f'current window size {self.root.winfo_width()} x {self.root.winfo_height()}'))
            self.chk_button.pack(pady=10, side=tk.LEFT)

    def create_dynamic_inputs(self, configurations, font):
        for config in configurations:
            frame = tk.Frame(self.root)
            frame.pack(pady=5)
            label = tk.Label(frame, width=20, text=config['name'], justify=tk.LEFT, anchor='w', font=font)
            label.pack(side=tk.LEFT)

            if config['type'] == 'option':
                var = tk.StringVar(frame)
                var.set(config['options'][0])  # set the default option
                entry = tk.OptionMenu(frame, var, *config['options'])
            elif config['type'] == 'text':
                entry = tk.Entry(frame, width=10, justify=tk.RIGHT)
                if 'default' in config:
                    entry.insert(tk.END, str(config['default']))
            entry.pack(side=tk.RIGHT)
            self.entries[config['name']] = entry

    def set_btn(self):
        # Get the values from the text boxes
        try:
            values = {name: (entry.get() if isinstance(entry, tk.Entry) else entry.cget("text")) for name, entry in self.entries.items()}
            # Call the custom button command function with the input values
            self.button_command(values)
            # Disable the text boxes to prevent further input
            self.disable_textboxes()
        except ValueError:
            print("Please enter valid values.")

    def flip_btn(self, callbackFUNCstart, callbackFUNCstop): # no more needed because start/pause button is removed
        if self.set_button['state'] != tk.DISABLED:
            Status('Set Delay Time !')
            Action('ERROR')
            return
        if self.start_button['text'] == 'Start':
            callbackFUNCstart()
            self.start_button.config(text='Stop')
        else:
            callbackFUNCstop()
            self.start_button.config(text='Start')

    def disable_textboxes(self):
        # Disable the text boxes
        for entry in self.entries.values():
            entry.config(state='disabled')
        self.set_button.config(state=tk.DISABLED)
        Status('Configurations Updated')
        Action('')

    def SetStatus(self, mesg):
        try:
            self.title_label.config(text=mesg)
        except:
            pass
    def SetAction(self, mesg):
        try:
            self.subtitle_label.config(text=mesg)
        except:
            pass

class GUIConfigurables:
    def __init__(self, allCONF):
        self.configurations = allCONF

        self.startFUNC = lambda: print('start!!!')
        self.pauseFUNC = lambda: print('pause!!!')
        self.setFUNC = lambda values: print(f'[SetValue] {values}')

if __name__ == "__main__":
    def custom_button_set(values:dict):
        print(f"[MODIFIED] Button clicked with values: {values}")
    def custom_button_start():
        print(f"[MODIFIED] STARTTTTTTTT")
        Status('started')
    def custom_button_pause():
        print(f"[MODIFIED] PAUSED")
        Status('paused')

    all_configurations = [
        {'name': 'TTY Device', 'type': 'option', 'options': ['/dev/tty.usbmodem1101', '/dev/ttyaa']},
        {'name': 'Moving Delay', 'type': 'text', 'default': 3},
        {'name': 'Capturing Delay', 'type': 'text', 'default': 3}
    ]
    GUI_conf = GUIConfigurables(all_configurations)
    GUI_conf.setFUNC = custom_button_set
    GUI_conf.startFUNC = custom_button_start
    GUI_conf.pauseFUNC = custom_button_pause

    root = tk.Tk()
    app = CustomGUI(root, GUI_conf)
    Status = app.SetStatus
    Action = app.SetAction
    root.mainloop()
