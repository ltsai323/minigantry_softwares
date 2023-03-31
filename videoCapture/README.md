## execution
In linux, you can execute run.sh or check.sh by command.

* $run.sh$ is automatic mode. You need to specify wait time and number images captured. Press spacebar to start first photo and pause/continue the whole process by spacebar.
* $check.sh$ is manual mode. Press space bar to take photo.


In windows, run.bat and check.bat.







## installation
First of all, install python3 from Microsoft Store.
Then you can open powershell or cmd.exe to check python3.exe works or not.
If so, use pip3 command to install opencv.
```
# in power shell
python3.exe -m pip install --user python-opencv

# in bash
pip3 install --user python-opencv
sudo apt install python3-opencv
```

Then you can use "run.bat" to execute the program.

## Known issues
* [ ] For laptops, opencv will access the built in camera. Currently you can stop it and run the program.


