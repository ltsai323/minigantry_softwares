Build an exe file from .py file

## Environment Setup
* Install anaconda from website. (Currently Python3.9 64-Bit. conda version "conda 22.11.1")
* conda commands
    - conda create --name dxfREADER python=3.8
    - conda activate dxfREADER
    - conda install -c conda-forge ezdxf pyinstaller
    - conda install -c conda-forge::blas=*=openblas numpy
    - conda install  matplotlib
* package command
    - pyinstaller.exe --clean -F yourfile.py

Note that sortedPoint.py contains matplotlib. With this package, the packed executable size from 6.5MB to 299MB.
And executable size of dxfReader.py is 12.6MB.