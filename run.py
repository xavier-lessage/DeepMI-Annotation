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
INPUT_A = '/Users/nedo/Documents/angioai/annotation/disease'
INPUT_R = '/Users/nedo/Documents/angioai/annotation/disease'
OUTPUT = '/Users/nedo/Documents/angioai/annotation/out'
INDEX_FILE = '/Users/nedo/Documents/angioai/annotation/log/index.log'
REVIEW_FILE = '/Users/nedo/Documents/angioai/annotation/log/review.log'

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
        self.index = None
        self.currentAnnotationRectangle = None
        self.start_x = None
        self.start_y = None
        self.end_x = None
        self.end_y = None
        self.currentDefiningAnnotationColor = None
        self.currentDefiningAnnotationCode = None


        buttonNext = QPushButton()
        buttonNext.setText("Next [2]")
        buttonNext.clicked.connect(self.buttonNext_clicked)
        #button1.move(64, 32)
        #widget.setGeometry(50, 50, 320, 200)

        buttonPrevious = QPushButton()
        buttonPrevious.setText("Previous [1]")
        buttonPrevious.clicked.connect(self.buttonPrevious_clicked)

        buttonRedAnnotation = QPushButton()
        buttonRedAnnotation.setText("Red Annotation [Q]")
        buttonRedAnnotation.clicked.connect(self.buttonRedAnnotation_clicked)

        buttonOrangeAnnotation = QPushButton()
        buttonOrangeAnnotation.setText("Orange Annotation [W]")
        buttonOrangeAnnotation.clicked.connect(self.buttonOrangeAnnotation_clicked)

        buttonGreenAnnotation = QPushButton()
        buttonGreenAnnotation.setText("Green Annotation [E]")
        buttonGreenAnnotation.clicked.connect(self.buttonGreenAnnotation_clicked)

        buttonClear = QPushButton()
        buttonClear.setText("Clear Annotation(s) [C]")
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


        #define a text label
        self.progressLabel = QtWidgets.QLabel(self)
        self.progressLabel.setText("Progress: 0/0")
        
      


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
        layout.addWidget(self.progressLabel, 4, 0)

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

    def markStartXandY(self, event):
        # print("Mark Start X and Y")
        self.start_x = event.xdata
        self.start_y = event.ydata
        #disconnect the mouse event to avoid multiple calls
        self.sc.figure.canvas.mpl_disconnect(self.sc.figure.canvas.mpl_connect('motion_notify_event', self.markStartXandY))


    def startDefiningAnnotationArea(self,color,code):
        # print("Start Defining Annotation Area")
        
        self.currentDefiningAnnotationColor = color
        self.currentDefiningAnnotationCode = code
        #connect a mouse event to the canvas to get the start coordinates of the annotation area
        self.sc.figure.canvas.mpl_connect('motion_notify_event', self.markStartXandY)

        
        
        # print("Start x and y are " + str(self.start_x) + " " + str(self.start_y))

        
        #when the cursor moves on the canvas create a rectangle to mark the annotation area and update the rectangle coordinates
        self.sc.figure.canvas.mpl_connect('motion_notify_event', self.updateAnnotationArea)

        
        #when mouse is clicked on the canvas, call the function to mark the end of the annotation area
        #when mous is up on the canvas, call the function to mark the end of the annotation area
        self.sc.figure.canvas.mpl_connect('button_release_event', self.endDefiningAnnotationArea)
        # self.sc.figure.canvas.mpl_connect('button_press_event', self.endDefiningAnnotationArea)


    def updateAnnotationArea(self, event):
        # print("Update Annotation Area")
        # print("End x and y are " + str(event.xdata) + " " + str(event.ydata))
        #if currentAnnotationRectangle is not None, remove it from the canvas
        if self.currentAnnotationRectangle is not None:
            self.currentAnnotationRectangle.remove()

        #create a new rectangle to mark the annotation area that begins in the start_x and start_y and ends in the current cursor position
        self.currentAnnotationRectangle = patches.Rectangle((self.start_x, self.start_y), event.xdata - self.start_x, event.ydata - self.start_y, fill=False, edgecolor=self.currentDefiningAnnotationColor, linewidth=1)
        self.end_x = event.xdata
        self.end_y = event.ydata

        #add the new rectangle to the canvas
        self.sc.figure.gca().add_patch(self.currentAnnotationRectangle)
        #update the canvas
        self.sc.draw()



                

      

    def endDefiningAnnotationArea(self,event):
        # print("End Defining Annotation Area")
        #mark annotation end coordinates at current cursor position
        # self.end_x = event.xdata
        # self.end_y = event.ydata
        #disconnect the mouse click event
        self.sc.figure.canvas.mpl_disconnect(self.sc.figure.canvas.mpl_connect('button_press_event', self.endDefiningAnnotationArea))
        #call the function to draw the annotation area

        #convert coordinates from base 10 to integer and then to string

        start_x = str(int(float(self.start_x)))
        start_y = str(int(float(self.start_y)))
        end_x = str(int(float(self.end_x)))
        end_y = str(int(float(self.end_y)))
        #if the annotation area is not empty, update the annotation file
        if self.start_x != self.end_x and self.start_y != self.end_y:
            self.updateAnnotationFile(start_x, end_x, start_y, end_y,self.currentDefiningAnnotationColor,self.currentDefiningAnnotationCode)
        # #prevent the  updateAnnotationArea function to be called when the cursor moves
        #     self.sc.figure.canvas.mpl_disconnect(self.sc.figure.canvas.mpl_connect('motion_notify_event', self.updateAnnotationArea))
        #     #disconnect the button release event to avoid multiple calls
        #     self.sc.figure.canvas.mpl_disconnect(self.sc.figure.canvas.mpl_connect('button_release_event', self.endDefiningAnnotationArea))
        #     if self.currentAnnotationRectangle is not None:
        #         self.currentAnnotationRectangle.remove()
        #         self.currentAnnotationRectangle = None
        #     self.currentDefiningAnnotationColor = None
        #     self.currentDefiningAnnotationCode = None
        # self.drawAnnotationArea()
        self.cancelDefiningAnnotationArea()


    # def drawAnnotationArea(self):
        #  self.AnnotationGeneration('red', '1')


    def cancelDefiningAnnotationArea(self):
        # print("Cancel Defining Annotation Area")
        #disconnect the mouse click event
        self.sc.figure.canvas.mpl_disconnect(self.sc.figure.canvas.mpl_connect('button_press_event', self.endDefiningAnnotationArea))
        #prevent the  updateAnnotationArea function to be called when the cursor moves
        self.sc.figure.canvas.mpl_disconnect(self.sc.figure.canvas.mpl_connect('motion_notify_event', self.updateAnnotationArea))
        #disconnect the button release event to avoid multiple calls
        self.sc.figure.canvas.mpl_disconnect(self.sc.figure.canvas.mpl_connect('button_release_event', self.endDefiningAnnotationArea))
        if self.currentAnnotationRectangle is not None:
            self.currentAnnotationRectangle.remove()
            
            self.currentAnnotationRectangle = None
            self.sc.draw()
        self.currentDefiningAnnotationColor = None
        self.currentDefiningAnnotationCode = None

        

    def buttonRadioAnnotation_clicked(self):

        print("Button Mode Annotation clicked")
        self.setWindowTitle('DeepM-Annotation ' + '' + self.imageName)

        self.buttonPrevious_clicked()
        self.buttonNext_clicked()




    def buttonRadioReview_clicked(self):

        print("Button Mode Review clicked")
        self.setWindowTitle('DeepM-Review ' + '' + self.imageName)

        self.fichiers = []
        self.nbr_review = 0
        # r=root, d=directories, f = files
        for r, d, f in os.walk(INPUT_R):
            for file in f:
                if file.endswith("." + EXT):
                    print(os.path.join(r, file))
                    self.fichiers.append(file)
                    self.nbr_review = self.nbr_review + 1

        ReviewIndex = open(REVIEW_FILE, "w")
        ReviewIndex.write(str(1))
        ReviewIndex.close()
        print('self.nbr_review',self.nbr_review)

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
        self.updateAnnotationFile(x1, x2, y1, y2, classColor, classCode)

    def updateAnnotationFile(self,x1,x2,y1,y2, classColor, classCode):


 
        fileIndex = open(INDEX_FILE, "r")
        index = int(fileIndex.read())
        fileIndex.close()
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
            #fileReview = open(REVIEW_FILE, "w") ####
            #fileReview.write(str(INDEX))

            print(self.index_file)
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

        self.index = index
        self.updateProgressLabel(index)
        
        #print(fichiers[index])
        fileIndex = open(self.index_file, "w")
        fileIndex.write(str(index))
        fileIndex.close()
        self.imageName = fichiers[index]
        if self.windowTitle()[6] == 'R':
            try:
                self.imageName = self.fichiers[index]
            except:
                self.buttonRadioReview_clicked()
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
       
        self.index = index
        self.updateProgressLabel(index)

       

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


    def updateProgressLabel(self,index):
        self.progressLabel.setText(str(index) + "/" + str(len(fichiers)))


    def loadingFiles(self):



        # Load last image or fist for the first run
        if os.path.exists(INDEX_FILE):
            fileIndex = open(INDEX_FILE, "r")
            index = int(fileIndex.read())
        else:
            fileIndex = open(INDEX_FILE, "w")
            fileIndex.write(str(1))
            index = 1

        self.index = index
        self.updateProgressLabel(index)

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
        #if key 1 pressed call previous image
        if e.key() == Qt.Key.Key_1.value:
            self.buttonPrevious_clicked()
        #if key 2 pressed call next image
        if e.key() == Qt.Key.Key_2.value:
            self.buttonNext_clicked()

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
        # if e.key() == Qt.Key.Key_Q.value:
            # self.buttonOrangeAnnotation_clicked()
        # if Z key pressed call start defining annotation area
        if e.key() == Qt.Key.Key_Q.value:
            if self.currentDefiningAnnotationColor == None:
                self.startDefiningAnnotationArea('red',1)
            else:
                self.endDefiningAnnotationArea(e)
        # if C key pressed then call button clear 
        if e.key() == Qt.Key.Key_C.value:
            self.buttonClear_clicked()
        

        # same thing for w key but orange and 2
        if e.key() == Qt.Key.Key_W.value:
            if self.currentDefiningAnnotationColor == None:
                self.startDefiningAnnotationArea('orange',2)
            else:
                self.endDefiningAnnotationArea(e)
        # same thing for e key but green and 3
        if e.key() == Qt.Key.Key_E.value:
            if self.currentDefiningAnnotationColor == None:
                self.startDefiningAnnotationArea('green',3)
            else:
                self.endDefiningAnnotationArea(e)

        #if z button is pressed cancel defining annotation area
        if e.key() == Qt.Key.Key_Z.value:
            if self.currentDefiningAnnotationColor != None:
                self.cancelDefiningAnnotationArea()
            
        # if e.key() == Qt.Key.Key_W.value:
        #     self.buttonGreenAnnotation_clicked()


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
