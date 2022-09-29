#######################################################################
#######           Afficher images DICOM avec matplotlib         #######
#######################################################################

import matplotlib.pyplot as plt
from matplotlib import pylab
import pydicom
import easygui

## choix d'un fichier SOURCE dcm uniquement !!
SOURCE = easygui.fileopenbox()   

# Calcul valeur de gris minimum et maximum pour meilleur contraste à l'affichage

dataset = pydicom.dcmread(SOURCE) # lire métadonnées DICOM

# si CT calcul vmin et vmax spécifiques
if dataset.Modality == "CT": 
    level =  dataset.WindowCenter  # centre dans métadonnées
    window = dataset.WindowWidth # window dans méta
    vmin = 1000 + (level - window/2) # calcul de l'interval de gris !!! AJOUTER 1000 au level
    vmax = 1000 + (level + window/2)

# si MG calcul vmin et vmax spécifiques    
if dataset.Modality == "MG" and type(dataset.WindowCenter) is pydicom.multival.MultiValue:
    level =  dataset.WindowCenter[0] # centre dans méta
    window = dataset.WindowWidth[0] # window dans méta
    vmin = level - window/2 # calcul de l'interval de gris
    vmax = level + window/2 

# si CR calcul vmin et vmax
elif dataset.Modality == "CR":
    level =  dataset.WindowCenter # centre dans méta
    window = dataset.WindowWidth # window dans méta
    vmin = level - window/2 # calcul de l'interval de gris
    vmax = level + window/2 

#########################################################################

# affichage de l'image Dicom avec matplotlib
fig = plt.figure(figsize=(10, 30), dpi=300) ## dimension de l'image et résolution en dpi
fig.patch.set_facecolor('xkcd:black') ## choix de la couleur de fond
plt.axis('off') ## suppression des axes et annotations
plt.subplots_adjust(left=0, right=1, top=1, bottom=0, wspace=0, hspace=0) ## réduction des marges sup, inf, dr, g

# affiche pixel_array du dataset en échelle de gris et un définissant valeur de grix min et max
# sous vmin tout est noir
# au dessus de vmax tout est blanc
plt.imshow(dataset.pixel_array, cmap="gray", vmin=vmin, vmax=vmax)
plt.show()


        

        

