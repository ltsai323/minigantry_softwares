#!/usr/bin/env bash

python3 videoCapture.py GPIO

echo output dir:
ls -l | head -n1
read -p "press enter to continue"
