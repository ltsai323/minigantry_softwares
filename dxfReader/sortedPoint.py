#!/usr/bin/env python3
mesg='Shortest distance algorithm in mini gantry coordinate'

def PrintHelp():
    print('''
    ==================================================================
    === Usage :                                                    ===
    ===    dxfReader reads a text file. The text file should come  ===
    ===    from dxfReader.py. This code loads the center of CIRCLE ===
    ===    and translate coordinate from dxf file to mini gantry.  ===
    ===    Then sorts the points into shortest length.             ===
    ===    Args 1 : a txt file from dxfReader.py                   ===
    ===                                                            ===
    ===    Note output file would be stored at the same directory  ===
    ===    as input file.                                          ===
    ==================================================================
    ''')
    os.system('pause')
def GetArg_InputFile(argv):
    if len(argv) != 2:
        PrintHelp()
    return argv[1]

class MyPoint(object):
  def __init__(self, x,y):
    self.x=float(x)
    self.y=float(y)
  def __repr__(self):
    return '(%7.2f,%7.2f)'%(self.x,self.y)
  def Length(self,point):
    return ( (self.x-point.x)**2+(self.y-point.y)**2 )**0.5
def TranslatePointsFromLine(line):
  words=line.split()
  if len(words) < 2: return None
  return MyPoint(words[-2],words[-1])  
def TransformIntoMiniGantry(point):
  return MyPoint( -1.*point.y, point.x)
  
def SortingPoints(point_pool):
  MAXLEN_ACCEPTABLE=70
  BREAK_COUNTER=len(point_pool)*2

  import random
  while True:
    # shallow copy. Only copy the indexes of that list. all content indicates to the same values.
    pool=list(point_pool)
    # prepare a first point
    seedIdx=random.randint(0,len(pool)-1)

    p0=pool[seedIdx]
    pool.pop(seedIdx)
    # start the algorithm
    sorted=ShortedLength(p0,pool)
  
    sorted.append(p0)
    maxlen=max( [ sorted[i].Length(sorted[i+1]) for i in range(len(sorted)-1)] )

    BREAK_COUNTER-=1
    if BREAK_COUNTER == 0: raise RuntimeError("No solution for this algorithm! Please extend allowed value of 'MAXLEN_ACCEPTABLE' in SortingPoints()")
    if maxlen > MAXLEN_ACCEPTABLE: continue
    
    return sorted
  
# recursive function 
def ShortedLength(currentPoint, PointPool):
  if len(PointPool)==0: return []

  leng=9999.
  idxFound=-1
  for idx,nextPoint in enumerate(PointPool):
    if currentPoint.Length(nextPoint) < leng:
      leng=currentPoint.Length(nextPoint)
      idxFound=idx
  pointFound=PointPool[idxFound]
  PointPool.pop(idxFound)
  resultlist=ShortedLength( pointFound, PointPool )
  resultlist.append(pointFound)
  return resultlist

def DrawOutput(points, outputname):
  from matplotlib import pyplot
  import numpy as np
  
  xvals = np.array( [ point.x for point in points ] )
  yvals = np.array( [ point.y for point in points ] )
  #pyplot.scatter( xvals, yvals )
  #pyplot.xlabel('')
  pyplot.plot(xvals, yvals, '.r-')
  #pyplot.show()
  pyplot.savefig(outputname)


if __name__ == "__main__":
  import sys
  if len(sys.argv) != 2: raise IOError('input a text file!')
  print ( 'input file : %s' % sys.argv[1] )
  
  lines = ( line.strip() for line in open(sys.argv[1], 'r').readlines() if 'CIRCLE' in line )
  points = ( TranslatePointsFromLine(line) for line in lines if (TranslatePointsFromLine(line) != None ))
  convertedPoints = [ TransformIntoMiniGantry(point) for point in points ]
  for idx, cPoint in enumerate(convertedPoints):
    if abs(cPoint.x) < 1e-1 and abs(cPoint.y) < 1e-1:
      print('reference point found. remove it from point list')
      convertedPoints.pop(idx)

  print(mesg)
  sortedPoints = SortingPoints(convertedPoints)

  with open('output_sortedPoints.txt', 'w') as ofile:
    for idx,cPoint in enumerate(sortedPoints):
      # print to screen
      #print('No.%2d: %s'%(idx,cPoint))
      #if idx%5==5-1: print('---- 5 sep ----')
      
      # print to file
      ofile.write('No.%2d: %s\n'%(idx+1,cPoint))
      if idx%5==5-1: ofile.write('---- 5 sep ----\n')
  DrawOutput(sortedPoints, 'points_convertedToMiniGantry.png')

  print('output file is "output_sortedPoints.txt')
  import os
  os.system('pause')