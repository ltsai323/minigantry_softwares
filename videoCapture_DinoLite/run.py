#!/usr/bin/env python3
import bkg_process as bkg_job
#import GUIMgr
import bb as GUIMgr
import tkinter as tk
#import photo_capture_windows as photo_capture


DEFAULT_MOVING_DELAY = 4.0
DEFAULT_CAPTURING_DELAY = 0.5

if __name__ == "__main__":
    import sys
    #number_of_loops = int(sys.argv[1])

    #ps = bkg_job.ProgramStatus(number_of_loops)
    ps = bkg_job.API('data/bkg_process.yaml')


    def on_start():
        global ps
        ps.start()
    def on_pause():
        global ps
        ps.pause()
    def set_configurables(values:dict):
        global ps
        ps.set(**values)



    GUI_conf = GUIMgr.GUIConfigurables(ps.list_setting())
    GUI_conf.setFUNC = set_configurables
    GUI_conf.startFUNC = ps.start
    GUI_conf.pauseFUNC = ps.pause

    root = tk.Tk()
    myGUI = GUIMgr.CustomGUI(root, GUI_conf)

    bkg_job.SetLog(myGUI.SetStatus,myGUI.SetAction)
    # run bkg job
    #bkg_thread = bkg_job.bkg_run_job(ps)
    bkg_thread = ps.run()
    root.mainloop()

    # clear background job after close mark clicked
    ps.programStatus.programIsAlive.clear()
