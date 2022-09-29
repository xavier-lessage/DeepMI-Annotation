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
from pylab import imread

INPUT = '/Users/xle/Desktop/Shooting'
OUTPUT = '/Users/xle/Desktop/Annotation'
INDEX_FILE = '/Users/xle/Desktop/Annotation/index.log'
INDEX = 1

class MplCanvas(FigureCanvasQTAgg):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        buttonNext = QPushButton()
        buttonNext.setText("Next")
        buttonNext.clicked.connect(buttonNext_clicked)
        #button1.move(64, 32)
        #widget.setGeometry(50, 50, 320, 200)

        buttonPrevious = QPushButton()
        buttonPrevious.setText("Previous")
        buttonPrevious.clicked.connect(buttonPrevious_clicked)

        buttonAddAnnotation = QPushButton()
        buttonAddAnnotation.setText("Add Annotation")
        buttonAddAnnotation.clicked.connect(self.buttonAddAnnotation_clicked)

        buttonClear = QPushButton()
        buttonClear.setText("Clear Annotation(s)")
        buttonClear.clicked.connect(buttonClear_clicked)

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        #sc.figure.gca().axis('off')


        
        self.imageName = 'test.jpg'
        image = imread(self.imageName)
        self.sc.figure.gca().imshow(image)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(buttonPrevious)
        layout.addWidget(buttonNext)
        layout.addWidget(buttonAddAnnotation)
        layout.addWidget(buttonClear)
        layout.addWidget(self.sc)

        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()

        widget.setLayout(layout)

        self.setCentralWidget(widget)
        self.show()


    def buttonAddAnnotation_clicked(self):
        print("Button Add Annotation clicked")
        fileIndex = open(INDEX_FILE, "r")
        index = int(fileIndex.read())
        fileIndex.close()
        fileAnnotation = open(OUTPUT + "/" + fichiers[index].replace('jpeg', 'txt') , "w")
        fileAnnotation.write("Hello")
        fileAnnotation.close()
        print(self.imageName)
        self.imageName = 'test2.jpg'
        self.sc.figure.gca().imshow(imread(self.imageName))
        print(self.imageName)
        print(self.sc.figure.axes[0].viewLim._points[1, 1])
        #self.sc.figure.gca().clear()
        self.sc.draw()



def buttonNext_clicked():
        print("Button Next clicked")
        fileIndex = open(INDEX_FILE, "r")
        index = int(fileIndex.read())
        index = index + 1
        print(fichiers[index])
        fileIndex = open(INDEX_FILE, "w")
        fileIndex.write(str(index))
        fileIndex.close()


def buttonPrevious_clicked():
    print("Button Previous clicked")
    fileIndex = open(INDEX_FILE, "r")
    index = int(fileIndex.read())
    index = index - 1
    print(fichiers[index])
    fileIndex = open(INDEX_FILE, "w")
    fileIndex.write(str(index))
    fileIndex.close()





def buttonClear_clicked():
    print("Button Clear clicked")
    fileIndex = open(INDEX_FILE, "r")
    index = int(fileIndex.read())
    fileIndex.close()
    fileToDel = OUTPUT + "/" + fichiers[index].replace('jpeg', 'txt')
    if os.path.exists(fileToDel):
        os.remove(fileToDel)


if __name__ == "__main__":

    fichiers = [f for f in listdir(INPUT) if isfile(join(INPUT, f))]
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec()