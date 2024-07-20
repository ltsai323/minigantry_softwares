#!/usr/bin/env python3
import bkg_process as bkg_job
import GUIMgr
#import bb as GUIMgr
import tkinter as tk
#import photo_capture_windows as photo_capture


DEFAULT_MOVING_DELAY = 4.0
DEFAULT_CAPTURING_DELAY = 0.5

if __name__ == "__main__":
    import sys
    #number_of_loops = int(sys.argv[1])

    #ps = bkg_job.ProgramStatus(number_of_loops)
    #ps = bkg_job.API('data/bkg_process.yaml')
    ps = bkg_job.API('data/bkg_process_windows.yaml')
    #ps = bkg_job.API('bkg_process_windows.yaml')


    def on_start():
        global ps
        #ps.start()
        SecondaryLog('Start button is malfunctioning')
    def on_pause():
        global ps
        #ps.pause()
        SecondaryLog('Pause button is malfunctioning')
    def set_configurables(values:dict):
        global ps
        ps.set(**values)
        ps.standby()
    def force_stop():
        global ps
        PrimaryLog('Force Stopped')
        SecondaryLog('Force stopping the whole process...')
        ps.force_stop()



    GUI_conf = GUIMgr.GUIConfigurables(ps.list_setting())
    GUI_conf.setFUNC = set_configurables
    GUI_conf.startFUNC = ps.start
    GUI_conf.pauseFUNC = ps.pause

    root = tk.Tk()
    myGUI = GUIMgr.CustomGUI(root, GUI_conf)

    bkg_job.SetLog(myGUI.SetStatus,myGUI.SetAction)
    # run bkg job
    bkg_thread = ps.run()
    root.mainloop()

    # clear background job after close mark clicked
    ps.force_stop()
