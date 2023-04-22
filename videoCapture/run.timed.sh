#!/usr/bin/env bash

DELAYTIME=3
NUM_IMAGE=10


python3 videoCapture.py Timer $DELAYTIME $NUM_IMAGE

echo output dir:
ls -lt | head -n1
read -p "press enter to continue"
