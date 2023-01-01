import os
import sys
import matplotlib
matplotlib.use('Qt5Agg')

import PIL
from PIL import Image

from PyQt6 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QPushButton
from os import listdir
from os.path import isfile, join
from matplotlib.pyplot import imread
from matplotlib import patches
from PyQt6.QtCore import Qt



import shutil

#DATA_IN= '/Users/xle/Desktop/these/mammo/in/positifs_masses'
IN = '/Users/xle/Desktop/these/yolo/datasets/Penguins_data/labels/test/'
OUT = '/Users/xle/Desktop/these/yolo/datasets/Penguins_data/labels/'

#INDEX_FILE = '/Users/xle/Desktop/these/mammo/log/index.log'
#INDEX = 1
#EXT = 'png'

if __name__ == "__main__":
    # List all files
    for f in listdir(IN):
        if isfile(join(IN, f)):
            if f.endswith('.txt'):
                #print(f)

                with open(join(IN, f)) as a:
                    line = a.readline().rstrip()

                    #print(line)

                    nc = line.split(' ')[0]
                    print(nc)

                    cx = line.split(' ')[1]

                    print(cx)

                    cy = line.split(' ')[2]

                    print(cy)

                    x = line.split(' ')[3]

                    print(x)

                    y = line.split(' ')[4]

                    print(y)

                    with open(join(OUT, f), 'w') as t:
                        annotation = '0 ' + str(cx) + ' ' + str(cy) + ' ' + str(x) + ' ' + str(y)
                        t.write(annotation)
