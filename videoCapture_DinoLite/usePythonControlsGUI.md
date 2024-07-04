# Use Python Controls GUI
## GUI Control by Hotkey
* [ ] Python activates program
* [ ] Python sends hotkey to specific program
* [ ] Once the foreground program is modified, is it able to keep sending hotkey to correct program?
## Make 3 buttons handling the capture status
* [x] Use PyQt5 for a small toolbox
* [x] Show the captured image index
* [ ] Show Status and Action message
* [ ] Handling x mark behaviour
* [ ] Disable button at current situation
* [ ] Handling two line message
* [x] background update message
* [ ] Use button trigger the bkg running flag

## Send information to serial device
* [ ] Python sends trigger to mini gantry through GPIO port on Raspberry Pi Pico
* [ ] Design a mechanism for this
  - [x] Open GUI and waiting for status
  - [ ] Send trigger to mini gantry for next movement
  - [x] waiting for mini gantry moving to new position
  - [ ] send hotkey capturing photo
  - [x] waiting for capturing procedure

