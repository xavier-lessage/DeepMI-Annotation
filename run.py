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
from matplotlib import patches
from PyQt6.QtCore import Qt

INPUT = '/Users/xle/Desktop/Angiographies/Disease'
OUTPUT = '/Users/xle/Desktop/Annotation'
INDEX_FILE = '/Users/xle/Desktop/Annotation/index.log'
INDEX = 1
EXT = 'png'

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
        buttonNext.clicked.connect(self.buttonNext_clicked)
        #button1.move(64, 32)
        #widget.setGeometry(50, 50, 320, 200)

        buttonPrevious = QPushButton()
        buttonPrevious.setText("Previous")
        buttonPrevious.clicked.connect(self.buttonPrevious_clicked)

        buttonRedAnnotation = QPushButton()
        buttonRedAnnotation.setText("Red Annotation")
        buttonRedAnnotation.clicked.connect(self.buttonRedAnnotation_clicked)

        buttonOrangeAnnotation = QPushButton()
        buttonOrangeAnnotation.setText("Orange Annotation")
        buttonOrangeAnnotation.clicked.connect(self.buttonOrangeAnnotation_clicked)

        buttonGreenAnnotation = QPushButton()
        buttonGreenAnnotation.setText("Green Annotation")
        buttonGreenAnnotation.clicked.connect(self.buttonGreenAnnotation_clicked)

        buttonClear = QPushButton()
        buttonClear.setText("Clear Annotation(s)")
        buttonClear.clicked.connect(self.buttonClear_clicked)

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.figure.gca().axis('off')

        self.line_color = 'orange'

        self.loadingFiles()
        #self.imageName = ''
        image = imread(INPUT + '/' + self.imageName)
        self.sc.figure.gca().imshow(image)

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        self.sc.figure.set_facecolor('black')

        layout = QtWidgets.QGridLayout()

        layout.addWidget(toolbar,0,0,1,0)
        layout.addWidget(buttonClear, 3, 0)
        layout.addWidget(buttonPrevious,3,1)
        layout.addWidget(buttonNext,3,2)
        layout.addWidget(buttonRedAnnotation,3,3)
        layout.addWidget(buttonOrangeAnnotation,3,4)
        layout.addWidget(buttonGreenAnnotation,3,5)
        layout.addWidget(self.sc,2,0,1,0)



        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        # set the title
        self.setWindowTitle('DeepM-Annotation ' + '' + self.imageName)

        #self.sc.figure.gca().axis('off')

        self.setCentralWidget(widget)
        self.show()




    def reloadAnnotation(self):
        print("Reload Annotation")
        if os.path.exists(OUTPUT + '/' + str(self.imageName).replace(EXT, 'log')):

            fileAnnotation= open(OUTPUT + '/' + str(self.imageName).replace(EXT, 'log'), "r")
            #print(str(self.imageName))
            fileAnnotation.readline()
            fileAnnotation.readline()

            while True:
                line = fileAnnotation.readline()
                if not line:
                    break
                print(line.strip())
                import re

                match = re.findall(r'[^\s,]+', line.strip())
                classe = match[0]
                x1 = match[1]
                x2 = match[2]
                y1= match[3]
                y2 = match[4]

                if classe == 'red':
                    self.line_color = 'red'
                if classe == 'orange':
                    self.line_color = 'orange'
                if classe == 'green':
                    self.line_color = 'green'

                self.sc.figure.gca().add_artist(
                    patches.mlines.Line2D([int(x1), int(x1)], [int(y1), int(y2)], color=self.line_color, linestyle='solid',
                                          linewidth=1))
                self.sc.figure.gca().add_artist(
                    patches.mlines.Line2D([int(x1), int(x2)], [int(y1), int(y1)], color=self.line_color, linestyle='solid',
                                          linewidth=1))
                self.sc.figure.gca().add_artist(
                    patches.mlines.Line2D([int(x2), int(x2)], [int(y1), int(y2)], color=self.line_color, linestyle='solid',
                                          linewidth=1))
                self.sc.figure.gca().add_artist(
                    patches.mlines.Line2D([int(x1), int(x2)], [int(y2), int(y2)], color=self.line_color, linestyle='solid',
                                          linewidth=1))
                self.sc.figure.gca().axis('off')
                self.sc.draw()


            fileAnnotation.close()

    def buttonRedAnnotation_clicked(self):

        print("Button Red Annotation clicked")
        self.AnnotationGeneration('red', '1')
        #self.reloadAnnotation()

    def buttonOrangeAnnotation_clicked(self):

        print("Button Orange Annotation clicked")
        self.AnnotationGeneration('orange', '2')
        #self.reloadAnnotation()

    def buttonGreenAnnotation_clicked(self):

        print("Button Green Annotation clicked")
        self.AnnotationGeneration('green', '3')
        #self.reloadAnnotation()

    def AnnotationGeneration(self,classColor, classCode):

        fileIndex = open(INDEX_FILE, "r")
        index = int(fileIndex.read())
        fileIndex.close()

        # Retrieval of coordinates
        x1 = str(int(self.sc.figure.axes[0].viewLim._points[0, 0]))
        #print(x1)
        x2 = str(int(self.sc.figure.axes[0].viewLim._points[1, 0]))
        #print(x2)
        y1 = str(int(self.sc.figure.axes[0].viewLim._points[0, 1]))
        #print(y1)
        y2 = str(int(self.sc.figure.axes[0].viewLim._points[1, 1]))
        #print(y2)



        # Update annotation file

        if os.path.exists(OUTPUT + "/" + fichiers[index].replace(EXT, 'log')):
            fileAnnotation = open(OUTPUT + "/" + fichiers[index].replace(EXT, 'log'), "a")
        else:
            fileAnnotation = open(OUTPUT + "/" + fichiers[index].replace(EXT, 'log'), "w")
            fileAnnotation.write(str(self.imageName + '\n'))
            fileAnnotation.write('classColor,x1,x2,y1,y2' + '\n')

        fileAnnotation.write(classColor + ',' + x1 + ',' + x2 + ',' + y1 + ',' + y2 + '\n')
        fileAnnotation.close()

        # Update annotation file (yolo format)
        # class x_center y_center width height
        if os.path.exists(OUTPUT + "/" + fichiers[index].replace(EXT, 'txt')):
            fileAnnotation = open(OUTPUT + "/" + fichiers[index].replace(EXT, 'txt'), "a")
        else:
            fileAnnotation = open(OUTPUT + "/" + fichiers[index].replace(EXT, 'txt'), "w")
            fileAnnotation.write(str(self.imageName + '\n'))

        x_center = str((int(x1) + int(x2) ) / 2)
        y_center = str((int(y1) + int(y2)) / 2)
        width = str(abs(int(x2) - int(x1)))
        height = str(abs(int(y2) - int(y1)))
        fileAnnotation.write(str(classCode) + ' ' + x_center + ' ' + y_center + ' ' + width + ' ' + height + '\n')
        fileAnnotation.close()

        #self.sc.figure.gca().clear()
        self.sc.figure.gca().axis('off')
        self.sc.draw()

        if classColor == 'red':
            self.line_color = 'red'
        if classColor == 'orange':
            self.line_color = 'orange'
        if classColor == 'green':
            self.line_color = 'green'

        self.sc.figure.gca().add_artist(patches.mlines.Line2D([int(x1), int(x1)], [int(y1), int(y2)], color=self.line_color, linestyle='solid', linewidth=1))
        self.sc.figure.gca().add_artist(patches.mlines.Line2D([int(x1), int(x2)], [int(y1), int(y1)], color=self.line_color, linestyle='solid',linewidth=1))
        self.sc.figure.gca().add_artist(patches.mlines.Line2D([int(x2), int(x2)], [int(y1), int(y2)], color=self.line_color, linestyle='solid',linewidth=1))
        self.sc.figure.gca().add_artist(patches.mlines.Line2D([int(x1), int(x2)], [int(y2), int(y2)], color=self.line_color, linestyle='solid',linewidth=1))

        #self.sc.figure.gca().axis('off')
        #self.sc.draw()

        self.sc.figure.gca().clear()
        image = imread(INPUT + '/' + self.imageName)
        self.setWindowTitle('DeepM-Annotation ' + '' + self.imageName)
        self.sc.figure.gca().imshow(image)
        self.reloadAnnotation()
        self.sc.figure.gca().axis('off')
        self.sc.draw()

    def buttonNext_clicked(self):
            print("Button Next clicked")
            fileIndex = open(INDEX_FILE, "r")
            index = int(fileIndex.read())
            index = index + 1
            print(fichiers[index])
            fileIndex = open(INDEX_FILE, "w")
            fileIndex.write(str(index))
            fileIndex.close()
            self.imageName = fichiers[index]
            image = imread(INPUT + '/' + self.imageName)
            self.setWindowTitle('DeepM-Annotation ' + '' + self.imageName)
            self.sc.figure.gca().clear()
            self.sc.figure.gca().imshow(image)
            self.reloadAnnotation()
            self.sc.figure.gca().axis('off')
            self.sc.draw()


    def buttonPrevious_clicked(self):
        print("Button Previous clicked")
        fileIndex = open(INDEX_FILE, "r")
        index = int(fileIndex.read())
        index = index - 1
        print(fichiers[index])
        fileIndex = open(INDEX_FILE, "w")
        fileIndex.write(str(index))
        fileIndex.close()
        self.imageName = fichiers[index]
        image = imread(INPUT + '/' + self.imageName)
        self.setWindowTitle('DeepM-Annotation ' + '' + self.imageName)
        self.sc.figure.gca().clear()
        self.sc.figure.gca().imshow(image)
        self.reloadAnnotation()
        self.sc.figure.gca().axis('off')
        self.sc.draw()




    def buttonClear_clicked(self):
        print("Button Clear clicked")
        fileIndex = open(INDEX_FILE, "r")
        index = int(fileIndex.read())
        fileIndex.close()
        fileTxtToDel = OUTPUT + "/" + fichiers[index].replace(EXT, 'txt')
        if os.path.exists(fileTxtToDel):
            os.remove(fileTxtToDel)
        fileLogToDel = OUTPUT + "/" + fichiers[index].replace(EXT, 'log')
        if os.path.exists(fileLogToDel):
            os.remove(fileLogToDel)
        self.sc.figure.gca().clear()
        image = imread(INPUT + '/' + self.imageName)
        self.sc.figure.gca().imshow(image)
        self.reloadAnnotation()
        self.sc.figure.gca().axis('off')
        self.sc.draw()

    def loadingFiles(self):

        # Load last image or fist for the first run
        if os.path.exists(INDEX_FILE):
            fileIndex = open(INDEX_FILE, "r")
            index = int(fileIndex.read())
        else:
            fileIndex = open(INDEX_FILE, "w")
            fileIndex.write(str(1))
            index = 1

        fileIndex.close()
        self.imageName = fichiers[index]
        print(fichiers[index])
        fileIndex.close()
        self.reloadAnnotation()
        self.sc.figure.tight_layout(h_pad=None)



    def keyPressEvent(self, e):

        if e.key() == Qt.Key.Key_Escape.value:
            self.close()
        if e.key() == Qt.Key.Key_Left.value:
            self.buttonPrevious_clicked()
        if e.key() == Qt.Key.Key_Right.value:
            self.buttonNext_clicked()
        if e.key() == Qt.Key.Key_Space.value:
            self.buttonNext_clicked()
        if e.key() == Qt.Key.Key_R.value:
            self.buttonRedAnnotation_clicked()
        if e.key() == Qt.Key.Key_O.value:
            self.buttonOrangeAnnotation_clicked()
        if e.key() == Qt.Key.Key_G.value:
            self.buttonGreenAnnotation_clicked()
        if e.key() == Qt.Key.Key_A.value:
            self.buttonRedAnnotation_clicked()
        if e.key() == Qt.Key.Key_Q.value:
            self.buttonOrangeAnnotation_clicked()
        if e.key() == Qt.Key.Key_W.value:
            self.buttonGreenAnnotation_clicked()

if __name__ == "__main__":
    # List all files
    fichiers = [f for f in listdir(INPUT) if isfile(join(INPUT, f))]
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec()
