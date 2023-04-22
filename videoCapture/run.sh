#!/usr/bin/env bash

python3 videoCapture.py GPIO

echo output dir:
ls -lt | head -n1
read -p "press enter to continue"
