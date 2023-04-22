#!/usr/bin/env bash

defaultDirName=`date +"capture_%d%B_%Y__%T"`
outputDir=${1:-${defaultDirName}}


python3 videoCapture.py Manual
mv tmpdir $outputDir

echo image captured at : $outputDir
read -p "press enter to continue"
