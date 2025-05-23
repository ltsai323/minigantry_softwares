#!/usr/bin/env python3
import re

class Point:
    identifier = 'MyPoint'
    def __init__(self, xPOINT, yPOINT):
        self.x_point = xPOINT
        self.y_point = yPOINT
    @property
    def x(self): return self.x_point
    @property
    def y(self): return self.y_point

    def __str__(self): return f'Point({self.x},{self.y})'
    def __repr__(self): return self.__str__()



def get_point(lineCONTENT) -> Point:
    if Point.identifier not in lineCONTENT: return None
    input_string = lineCONTENT.strip()
# Use a regular expression to find the numbers
    match = re.search(r'\(\s*([-\d.]+),\s*([-\d.]+)\)', input_string)

    if match:
        x = float(match.group(1))  # Extract the first number as x
        y = float(match.group(2))  # Extract the second number as y
        return Point(x,y)
    else:
        print(f'[NoMatched] line "{input_string}" does not matched anything')
        return None

class Line:
    identifier = 'MyLine'
    def __init__(self, startX, startY, endX, endY):
        self.start = Point(startX,startY)
        self.end   = Point(endX, endY)
    @property
    def plotx(self): return [self.start.x,self.end.x]
    @property
    def ploty(self): return [self.start.y,self.end.y]

def get_line(lineCONTENT) -> Line:
    if Line.identifier not in lineCONTENT: return None
    input_string = lineCONTENT.strip()
# Use a regular expression to find the numbers
    match = re.search(r'\(\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+),\s*([-\d.]+)\)', input_string)

    if match:
        startx = float(match.group(1))  # Extract the first number as x
        starty = float(match.group(2))  # Extract the second number as y
        endx   = float(match.group(3))  # Extract the first number as x
        endy   = float(match.group(4))  # Extract the second number as y
        return Line(startx,starty,endx,endy)
    else:
        print(f'[NoMatched] line "{input_string}" does not matched anything')
        return None


def recorded_points(iFILE):
    points = []
    with open(iFILE, 'r') as fIN:
        line = 1
        while line:
            line = fIN.readline()
            p = get_point(line)
            if '(' not in line or ')' not in line: continue
            if p: points.append(p)
    return points

def recorded_lines(iFILE):
    points = []
    with open(iFILE, 'r') as fIN:
        line = 1
        while line:
            line = fIN.readline()
            p = get_line(line)
            if '(' not in line or ')' not in line: continue
            if p: points.append(p)
    return points


import matplotlib.pyplot as plt
import numpy as np

def draw_plots(points:list,lines:list):
    x = [ p.x for p in points ]
    y = [ p.y for p in points ]
# Create the scatter plot
    fig, ax = plt.subplots()
    sc = ax.scatter(x, y, color='blue')
    sc2= ax.plot(x, y, '.r-')
    plotlines = [ ax.plot(l.plotx, l.ploty, 'black') for l in lines ]

# Annotate clicked point
    annot = ax.annotate("", xy=(0,0), xytext=(10,10), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    annot.set_visible(False)

    def update_annot(ind):
        pos = sc.get_offsets()[ind["ind"][0]]
        annot.xy = pos
        text = f"Index: {ind['ind'][0]+1}"
        annot.set_text(text)
        annot.get_bbox_patch().set_alpha(0.7)

    def on_click(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = sc.contains(event)
            print(ind)
            if cont:
                update_annot(ind)
                annot.set_visible(True)
                fig.canvas.draw_idle()
            else:
                if vis:
                    annot.set_visible(False)
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("button_press_event", on_click)

    ax.set_title("Click on a point to show its index")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.show()





if __name__ == "__main__":
    import sys
    inFILE = sys.argv[1]
    points = recorded_points(inFILE)
    lines  = recorded_lines (inFILE)
    draw_plots(points,lines)
