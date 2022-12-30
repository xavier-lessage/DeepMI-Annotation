import os
import sys
import matplotlib
matplotlib.use('Qt5Agg')

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

DATA_IN= '/Users/xle/Desktop/these/mammo/in/positifs_masses'
#DATA_IN = '/Users/xle/Desktop/these/mammo/in/negatifs'
INPUT = '/Users/xle/Desktop/these/mammo/out/'
DATA_OUT = '/Users/xle/Desktop/these/mammo/data/'
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



