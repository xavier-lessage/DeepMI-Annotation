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
DATA_IN = '/Users/xle/Desktop/these/mammo/in/negatifs'
INPUT = '/Users/xle/Desktop/these/mammo/out/'
DATA_OUT = '/Users/xle/Desktop/these/mammo/data/'
DATA_OUT_NORM = '/Users/xle/Desktop/these/mammo/outn/'
#INDEX_FILE = '/Users/xle/Desktop/these/mammo/log/index.log'
#INDEX = 1
#EXT = 'png'

if __name__ == "__main__":
    # List all files
    for f in listdir(INPUT):
        if isfile(join(INPUT, f)):
            if f.endswith('.txt'):
                #print(f)
                (prefix, sep, suffix) = f.rpartition('.')
                p = prefix + '.png'
                #print(join(DATA_IN, p))

                if isfile(join(DATA_IN, p)):
                    shutil.copyfile(join(DATA_IN, p), join(DATA_OUT, p))
                    shutil.copyfile(join(INPUT, f), join(DATA_OUT, f))



                    # loading the image
                    img = PIL.Image.open(join(DATA_IN, p))

                    # fetching the dimensions
                    wid, hgt = img.size

                    #print(p, wid, hgt)

                    with open(join(INPUT, f)) as a:
                        line = a.readline().rstrip()
                        line = a.readline().rstrip()

                        #print(line)

                        nc = line.split(' ')[0]
                        print(nc)

                        cx = line.split(' ')[1]
                        cxn = round(float(cx) / wid, 2)
                        print(cxn)

                        cy = line.split(' ')[2]
                        cyn = round(float(cy) / hgt, 2)
                        print(cyn)

                        x = line.split(' ')[3]
                        xn = round(float(x) / wid, 2)
                        print(xn)

                        y = line.split(' ')[4]
                        yn = round(float(y) / hgt, 2)
                        print(yn)

                        print(join(DATA_OUT_NORM, f))

                        with open(join(DATA_OUT_NORM, f), 'w') as t:
                            annotation = str(nc) + ' ' + str(cxn) + ' ' + str(cyn) + ' ' +str(xn) + ' ' + str(yn)
                            t.write(annotation)



