# Study history of Raspberry Pi Pico

## Software installation

* **Install ampy -** Command line interface controls raspberry Pi Pico.(ps1)

` pip3 install adafruit-ampy --user `

* **Install rshell -** shell of raspberry Pi Pico.(ps1)

` pip3 install rshell --user `

* **Update MicroPython firmware -**
Download firmware on [offical website]()

**ps1:** Notice that these tools cannot be installed in anaconda.

## copy file into raspberry pi pico

```bash
ampy --port /dev/tty.usbmodem1101  put helloworld_LEDblink.py  /main.py
```

While raspberry pi boots up / resets, the machine loads boots.py and main.py automatically.

* **/boot.py -** Some configurations, users usally does not need to modify this code. The description of this file from [documentation](https://learn.adafruit.com/micropython-basics-load-files-and-run-code).
    > This file is run first on power up/reset and should contain low-level code that sets up the board to finish booting. You typically don't need to modify boot.py unless you're customizing or modifying MicroPython itself. However it's interesting to look at the contents of the file to see what happens when the board boots up. Remember you can use the ampy get command to read this and any other file!
* **/main.py -** Our main function. executed on rebooted.
    > If this file exists it's run after boot.py and should contain any main script that you want to run when the board is powered up or reset.
* **other files -** Just put into the storage in raspberry pi pico.

## Execute code on pico temporally

```bash
ampy --port /dev/tty.usbmodem1101  run helloworld_LEDblink.py
```

Directly execute PC code on raspberry pi pico. This command stopped original code and execute new code. However, this code is temporally executed. The execution vanished once the machine is powered off or reseted.

## Access Shell of Raspberry Pi Pico

```bash
#!/usr/bin/env sh
rshell -p /dev/tty.usbmodem1101
```

# Usage
Execute this code searching raspberry pi pico candidate. List the option and choose manually (No option if only one candidate found)

```python3
./put_code_to_pico.py
```
