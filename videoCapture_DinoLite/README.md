
## installation
```
pip3 install pyserial pyyaml
pip3 install pyautogui pywin32
```


### Windows
#### Initialize
1. Install Python3 from **Microsoft Store**
1. Install [VcXsrv](https://sourceforge.net/projects/vcxsrv/)
1. Install [Dino Capture 2.0](https://dino-lite.cc/rjxz) ** Not to use 3.0 ##
1. **init.bat** install python dependencies and create [data/bkg_process_windows.yaml](https://github.com/ltsai323/minigantry_softwares/blob/main/videoCapture_DinoLite/data/bkg_process_windows.yaml) file according to the system.
#### Running
1. Download [VcXsrv configuration](https://github.com/ltsai323/NTUMAC_dockerized_softwares/blob/master/config.xlaunch) and execute this configuration everytime.
1. **run.bat** execute program


### MacOS
1. Install and open XQuarts
2. Install Dino Capture
3.  `sh run.sh`


### Debug
#### Modify configuration file
The default configurations are stored into [data/bkg_process_windows.yaml](https://github.com/ltsai323/minigantry_softwares/blob/main/videoCapture_DinoLite/data/bkg_process_windows.yaml). You can modify the values if needed.
#### Choose corrected serial port
This program searches the listed serial port from computer. Choose the serial port related to Raspberry Pi Pico from GUI.

## Special Note
*** Use Dino Capture 2.0 instead of 3.0 because only 2.0 accepts hotkey sent from python script. ***
