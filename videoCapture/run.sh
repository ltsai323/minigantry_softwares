#!/usr/bin/env bash

defaultDirName=`date +"capture_%d%B_%Y__%T"`
outputDir=${1:-${defaultDirName}}

DELAYTIME=3
NUM_IMAGE=10


python3 videoCapture.py $DELAYTIME $NUM_IMAGE
mv tmpdir $outputDir

echo image captured at : $outputDir
read -p "press enter to continue"
