import os
import sys
import PIL
import shutil
import matplotlib

matplotlib.use('Qt5Agg')

from PyQt6 import QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QPushButton, QRadioButton
from os import listdir
from os.path import isfile, join
from matplotlib.pyplot import imread
from matplotlib import patches
from PyQt6.QtCore import Qt

INPUT = ''
INPUT_A = '/Users/xle/Dataset/angiographies/Disease'
INPUT_R = '/Users/xle/Dataset/angiographies/out'
OUTPUT = '/Users/xle/Dataset/angiographies//out/'
INDEX_FILE = '/Users/xle/Dataset/angiographies/log/index.log'
REVIEW_FILE = '/Users/xle/Dataset/angiographies/log/review.log'


#INPUT = '/Users/xle/Desktop/these/mammo/in/negatifs'
#OUTPUT = '/Users/xle/Desktop/these/mammo/out/'
#INDEX_FILE = '/Users/xle/Desktop/these/mammo/log/index.log'
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

        self.fichiers = None
        self.index_file = None


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

        buttonRedDetect= QPushButton()
        buttonRedDetect.setText("Red Detection")
        buttonOrangeDetect = QPushButton()
        buttonOrangeDetect.setText("Orange Detection")
        buttonGreenDetect = QPushButton()
        buttonGreenDetect.setText("Green Detection")

        buttonRadioAnnotation = QRadioButton('Annotation')
        buttonRadioAnnotation.setChecked(True)
        buttonRadioAnnotation.clicked.connect(self.buttonRadioAnnotation_clicked)
        buttonRadioReview = QRadioButton('Review')
        buttonRadioReview.setChecked(False)
        buttonRadioReview.clicked.connect(self.buttonRadioReview_clicked)



        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.figure.gca().axis('off')

        self.line_color = 'orange'

        self.loadingFiles()

        image = imread(INPUT + '/' + self.imageName)
        self.sc.figure.gca().imshow(image, cmap="gray")

        # Create toolbar, passing canvas as first parament, parent (self, the MainWindow) as second.
        toolbar = NavigationToolbar(self.sc, self)

        #self.sc.figure.set_facecolor('darkgrey')
        self.sc.figure.set_facecolor('black')

        layout = QtWidgets.QGridLayout()

        layout.addWidget(toolbar, 0, 0, 1, 0)
        layout.addWidget(buttonClear, 3, 0)

        layout.addWidget(buttonRedAnnotation, 3, 3)
        layout.addWidget(buttonOrangeAnnotation, 3, 4)
        layout.addWidget(buttonGreenAnnotation, 3, 5)
        layout.addWidget(self.sc, 2, 0, 1, 0)
        #layout.addWidget(buttonReviewAnnotation, 4, 0)
        layout.addWidget(buttonRadioReview, 0, 4)
        layout.addWidget(buttonRadioAnnotation, 0, 5)

        layout.addWidget(buttonPrevious, 3, 1)
        layout.addWidget(buttonNext, 3, 2)
        #layout.addWidget(buttonDetect, 4, 3, 1, 3)
        layout.addWidget(buttonRedDetect, 4, 3)
        layout.addWidget(buttonOrangeDetect, 4, 4)
        layout.addWidget(buttonGreenDetect, 4, 5)



        # Create a placeholder widget to hold our toolbar and canvas.
        widget = QtWidgets.QWidget()
        widget.setLayout(layout)

        # set the title
        self.setWindowTitle('DeepMI-Annotation ' + '' + self.imageName)

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

    def buttonRadioAnnotation_clicked(self):

        print("Button Mode Annotation clicked")
        self.setWindowTitle('DeepM-Annotation ' + '' + self.imageName)

        self.buttonPrevious_clicked()
        self.buttonNext_clicked()




    def buttonRadioReview_clicked(self):

        print("Button Mode Review clicked")
        self.setWindowTitle('DeepM-Review ' + '' + self.imageName)

        self.fichiers = []

        # r=root, d=directories, f = files
        for r, d, f in os.walk(INPUT_R):
            for file in f:
                if file.endswith("." + EXT):
                    print(os.path.join(r, file))
                    self.fichiers.append(file)

        ReviewIndex = open(REVIEW_FILE, "w")
        ReviewIndex.write(str(1))
        ReviewIndex.close()

        self.buttonPrevious_clicked()
        self.buttonNext_clicked()

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


    def AnnotationGeneration(self, classColor, classCode):

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

        print('NAME', self.imageName)


        # Update annotation file

        if self.windowTitle()[6] == 'R':
            if os.path.exists(OUTPUT + "/" + self.imageName.replace(EXT, 'log')):
                fileAnnotation = open(OUTPUT + "/" + self.imageName.replace(EXT, 'log'), "a")
                #self.buttonRadioReview_clicked()
                #self.buttonNext_clicked()
                #self.buttonPrevious_clicked()
            else:
                fileAnnotation = open(OUTPUT + "/" + self.imageName.replace(EXT, 'log'), "w")
                fileAnnotation.write(str(self.imageName + '\n'))
                fileAnnotation.write('classColor,x1,x2,y1,y2' + '\n')
                #self.buttonRadioReview_clicked()
                #self.buttonNext_clicked()
                #self.buttonPrevious_clicked()

        else:
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

        if self.windowTitle()[6] == 'R':
            if os.path.exists(OUTPUT + "/" + self.imageName.replace(EXT, 'txt')):
                fileAnnotation = open(OUTPUT + "/" + self.imageName.replace(EXT, 'txt'), "a")
            else:
                fileAnnotation = open(OUTPUT + "/" + self.imageName.replace(EXT, 'txt'), "w")
        else:
            if os.path.exists(OUTPUT + "/" + fichiers[index].replace(EXT, 'txt')):
                fileAnnotation = open(OUTPUT + "/" + fichiers[index].replace(EXT, 'txt'), "a")
            else:
                fileAnnotation = open(OUTPUT + "/" + fichiers[index].replace(EXT, 'txt'), "w")
                #fileAnnotation.write(str(self.imageName + '\n'))

        x_center = str((int(x1) + int(x2) ) / 2)
        y_center = str((int(y1) + int(y2)) / 2)
        width = str(abs(int(x2) - int(x1)))
        height = str(abs(int(y2) - int(y1)))

        img = PIL.Image.open(join(INPUT, self.imageName))

        # fetching the dimensions
        wid, hgt = img.size

        # Normalisation

        x_center_n = str(round(float(x_center) / float(wid), 3))
        y_center_n = str(round(float(y_center) / float(hgt), 3))
        width_n = str(round(float(width) / float(wid), 3))
        height_n = str(round(float(height) / float(hgt), 3))

        #fileAnnotation.write(str(classCode) + ' ' + x_center + ' ' + y_center + ' ' + width + ' ' + height + '\n')
        fileAnnotation.write(str(classCode) + ' ' + x_center_n + ' ' + y_center_n + ' ' + width_n + ' ' + height_n + '\n')
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
        if self.windowTitle()[6] == 'R':
            print("")
        else:
            self.setWindowTitle('DeepM-Annotation ' + '' + self.imageName)
        self.sc.figure.gca().imshow(image, cmap="gray")
        if self.windowTitle()[6] == 'R':
            self.buttonRadioReview_clicked()
            self.buttonNext_clicked()
            self.buttonPrevious_clicked()
        else:
            self.reloadAnnotation()
        self.sc.figure.gca().axis('off')
        self.sc.draw()

        # Copy of the source file
        shutil.copyfile(join(INPUT, self.imageName), join(OUTPUT, self.imageName))

    def buttonNext_clicked(self):

        self.index_file = INDEX_FILE

        if self.windowTitle()[6] == 'R':
            print('mode review')
            self.index_file = REVIEW_FILE

        #INDEX_F = INDEX_FILE

        #print("Button Next clicked")
        fileIndex = open(self.index_file, "r")
        index = int(fileIndex.read())
        index = index + 1
        #print(fichiers[index])
        fileIndex = open(self.index_file, "w")
        fileIndex.write(str(index))
        fileIndex.close()
        self.imageName = fichiers[index]
        if self.windowTitle()[6] == 'R':
            self.imageName = self.fichiers[index]
        image = imread(INPUT + '/' + self.imageName)
        #if self.windowTitle()[6] == 'A':
        #    self.setWindowTitle('DeepM-Annotation ' + '' + self.imageName)
        if self.windowTitle()[6] == 'R':
            self.setWindowTitle('DeepM-Review ' + '' + self.imageName)
        else:
            self.setWindowTitle('DeepM-Annotation ' + '' + self.imageName)

        self.sc.figure.gca().clear()
        self.sc.figure.gca().imshow(image, cmap="gray")
        #if self.windowTitle()[6] == 'R':
            #self.buttonRadioReview_clicked()
                # self.buttonNext_clicked()
                # self.buttonPrevious_clicked()
        #else:
        self.reloadAnnotation()
        self.sc.figure.gca().axis('off')
        self.sc.draw()


    def buttonPrevious_clicked(self):

        self.index_file = INDEX_FILE

        if self.windowTitle()[6] == 'R':
            print('mode review')
            self.index_file = REVIEW_FILE

        #INDEX_F = INDEX_FILE

        print("Button Previous clicked")
        fileIndex = open(self.index_file, "r")
        index = int(fileIndex.read())
        index = index - 1
        print(fichiers[index])
        fileIndex = open(self.index_file, "w")
        fileIndex.write(str(index))
        fileIndex.close()
        self.imageName = fichiers[index]
        if self.windowTitle()[6] == 'R':
            self.imageName = self.fichiers[index]
        image = imread(INPUT + '/' + self.imageName)
        #if self.windowTitle()[6] == 'A':
        #    self.setWindowTitle('DeepM-Annotation ' + '' + self.imageName)
        if self.windowTitle()[6] == 'R':
            self.setWindowTitle('DeepM-Review ' + '' + self.imageName)
        else:
            self.setWindowTitle('DeepM-Annotation ' + '' + self.imageName)
        self.sc.figure.gca().clear()
        self.sc.figure.gca().imshow(image, cmap="gray")
        self.reloadAnnotation()
        self.sc.figure.gca().axis('off')
        self.sc.draw()


    def buttonClear_clicked(self):
        print("Button Clear clicked")
        fileIndex = open(INDEX_FILE, "r")
        ###
        #if self.windowTitle()[6] == 'R':
        #    print('mode review')
        #    #self.index_file = REVIEW_FILE
        #    self.fileIndex = REVIEW_FILE
        #image = imread(INPUT + '/' + self.imageName)
        ###
        index = int(fileIndex.read())
        fileIndex.close()

        if self.windowTitle()[6] == 'R':
            fileTxtToDel = OUTPUT + "/" + self.imageName.replace(EXT, 'txt')
        else:
            fileTxtToDel = OUTPUT + "/" + fichiers[index].replace(EXT, 'txt')
        if os.path.exists(fileTxtToDel):
            os.remove(fileTxtToDel)

        if self.windowTitle()[6] == 'R':
            fileLogToDel = OUTPUT + "/" + self.imageName.replace(EXT, 'log')
        else:
            fileLogToDel = OUTPUT + "/" + fichiers[index].replace(EXT, 'log')
        if os.path.exists(fileLogToDel):
            os.remove(fileLogToDel)

        if self.windowTitle()[6] == 'R':
            filePngToDel = OUTPUT + "/" + self.imageName.replace(EXT, 'png')
        else:
            filePngToDel = OUTPUT + "/" + fichiers[index].replace(EXT, 'png')
        if os.path.exists(filePngToDel):
            os.remove(filePngToDel)

        if self.windowTitle()[6] == 'R':
            fileJpgToDel = OUTPUT + "/" + self.imageName.replace(EXT, 'jpg')
        else:
            fileJpgToDel = OUTPUT + "/" + fichiers[index].replace(EXT, 'jpg')
        if os.path.exists(fileJpgToDel):
            os.remove(filePngToDel)

        self.sc.figure.gca().clear()
        image = imread(INPUT + '/' + self.imageName)
        self.sc.figure.gca().imshow(image, cmap="gray")
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

    # Mode Annotation by default
    INPUT = INPUT_A
    # List all files
    fichiers = []
    #fichiers = [f for f in listdir(INPUT) if (isfile(join(INPUT, f)))]

    # r=root, d=directories, f = files
    for r, d, f in os.walk(INPUT):
        for file in f:
            if file.endswith("." + EXT):
                print(os.path.join(r, file))
                fichiers.append(file)

    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()
    app.exec()
