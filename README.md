# DeepMI-Annotation



This tool is part of the Deep Medical Imaging Suite in the context of AI innovation in medical imaging (PhD thesis @ UMONS).
MIT License.

## How to use this tools?

Edit run.py and specifying the following fields:

INPUT = '/Users/xle/Desktop/Angiographies/Disease' --> Location of images to be annotated

OUTPUT = '/Users/xle/Desktop/Annotation' --> Emplacement des fichiers d'annotations

INDEX_FILE = '/Users/xle/Desktop/Annotation/index.log' --> Name of application log file

EXT = 'png' --> Format of the images 

Using the <Zoom> button, zoom in on the area to be annotated and click on the desired annotation (Red, Orange, Green).
Two annotation files will be generated, a classic log file and another one, in Yolo format.

## Keyboard shortcuts

"Space bar" : To go to the next image

Button "A" or Button "R" : To make an annotation with a red rectangle

Button "Q" or Button "O" : To make an annotation with a orange rectangle

Button "W" or Button "G" : To make an annotation with a green rectangle

Here are two examples:

a) File in Yolo format

  20160527-pt-c1b44ea247-std-91c870fac4-seq-18-ang-p26.9-p25.7-f-00041.png

  1 276.0 93.0 42 36
  
  3 151.0 113.0 128 84
  
  1 186.0 107.5 28 27
  
  2 261.5 124.5 29 21


b) Log file

  20160527-pt-c1b44ea247-std-91c870fac4-seq-18-ang-p26.9-p25.7-f-00041.png
  
  classColor,x1,x2,y1,y2
  
  red,255,297,111,75
  
  green,87,215,155,71
  
  red,172,200,121,94
  
  orange,247,276,135,114
  
  
  

## Screenshot 

<img width="1091" alt="image" src="https://user-images.githubusercontent.com/25364805/193655681-213bb97b-c72d-4760-9a58-40328f83da40.png">
  
<img width="1064" alt="image" src="https://user-images.githubusercontent.com/25364805/194230382-193f777d-6e6d-4a75-9c87-4cf667dc8ad4.png">
  
<img width="1064" alt="image" src="https://user-images.githubusercontent.com/25364805/194231066-fffb760e-c8ad-4d38-a163-78a7adead0d7.png">



