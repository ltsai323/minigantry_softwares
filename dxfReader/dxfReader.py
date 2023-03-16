#!/usr/bin/env python3.8
#https://ezdxf.mozman.at/docs/introduction.html

from __future__ import division

import os, sys
import ezdxf

def PrintHelp(idx):
    if idx == 0: ## raise Help
        print('''
    ==================================================================
    === Usage :                                                    ===
    ===    dxfReader reads a dxf file. Reading the coordinate of   ===
    ===    everything in this dxf file without any transformation. ===
    ===    The output file is "output.txt".                        ===
    ===    Args 1 : a dxf file.                                    ===
    ===                                                            ===
    ===    Note output file would be stored at the same directory  ===
    ===    as input file.                                          ===
    ===    Note2. Be sure the dxf has corrected unit. The unit     ===
    ===    is assumed to be corrected from solidworks.             ===
    ===                                                            ===
    ==================================================================
    ''')
    if idx == 1: ## number of layer > 1
        print('''
    ==================================================================
    === Error 1 :                                                  ===
    ===     Number of layer in DXF file is not 1. Please use       ===
    ===     Solid Works to choose the corrected layer.             ===
    ===                                                            ===
    ==================================================================
    ''')
    if idx == 2: ## No circle found
        print('''
    ==================================================================
    === Error 3 :                                                  ===
    ===     Number of layer in DXF file is not 1. Please use       ===
    ===     Solid Works to choose the corrected layer.             ===
    ===                                                            ===
    ==================================================================
    ''')
    exit(128)
def checkInputDXF(ifile):
    try:
        doc = ezdxf.readfile("{}".format(ifile))
        if len(doc.layers) != 2: PrintHelp(1)

        msp = doc.modelspace()
        if len(msp.query("CIRCLE")) == 0 and len(msp.query("LWPOLYLINE")) != 0:
            PrintHelp(2)

    except IOError:
        print('Not a DXF file or a generic I/O error.')
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print('Invalid or corrupted DXF file.')
        sys.exit(2)


def GetArg_InputFile(argv):
    if len(argv) != 2:
        PrintHelp(0)
    return argv[1]

# helper function
def print_entity(e):
    if e.dxftype() == 'LINE':
        print("LINE on layer: %s" % e.dxf.layer)
        print("start point: %s" % e.dxf.start)
        print("end point: %s\n" % e.dxf.end)
    elif e.dxftype() == 'CIRCLE':
        print("CIRCLE on layer: %s" % e.dxf.layer)
        print("center point: %s" % e.dxf.center)
        print("radius: %s\n" % e.dxf.radius)
    elif e.dxftype() == 'ARC':
        print("ARC on layer: %s" % e.dxf.layer)
        print("center point: %s" % e.dxf.center)
        print("radius: %s" % e.dxf.radius)
        print("start point: %s" % e.start_point)
        print("end point: %s\n" % e.end_point)

def write_entity(e, f, last_end):
    # isDispense, cw/ccw, speed, start point x, start point y, end point x, end point y, center point x, center point y
    if e.dxftype() == 'LINE':
        f.write("{}\t{}\t{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n".format('LINE', 0, 0, 20, e.dxf.start[0], e.dxf.start[1], e.dxf.end[0], e.dxf.end[1], 0, 0) )
    elif e.dxftype() == 'CIRCLE':
        f.write("{}\t{}\t{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n".format('CIRCLE', 0, 0, 20, last_end[0], last_end[1], last_end[0], last_end[1], e.dxf.center[0], e.dxf.center[1] ))
    elif e.dxftype() == 'ARC':
        f.write("{}\t{}\t{}\t{}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\t{:.3f}\n".format('ARC', 0, 0, 20, e.start_point[0], e.start_point[1], e.end_point[0], e.end_point[1], e.dxf.center[0]-e.start_point[0], e.dxf.center[1]-e.start_point[1]) )


if __name__ == "__main__":
    ifile=GetArg_InputFile(sys.argv)

    checkInputDXF(ifile)
    doc = ezdxf.readfile(ifile)

    f = open("output_dxfReader.txt", "w")
    f.write("Type, Dispense, cw/ccw, speed, start_x, start_y, end_x, end_y, center_x, center_y\n")

    # iterate over all entities in modelspace
    msp = doc.modelspace()
    # offical recommended usage
    #for circle in msp.query("CIRCLE"):
    #    print(circle.dxf.center)
    last_end=(0,0,0)
    for e in msp:
        write_entity(e, f, last_end)
    f.close()
    print('output file is output_dxfReader.txt')


