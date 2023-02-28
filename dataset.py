import os
import shutil

# this script will generate dataset from the images and the labels
# define source directory for annotations
ANNOTATIONS_DIR = '/Users/nedo/Documents/angioai/annotation/out'
# define source directory for images
IMAGES_DIR = '/Users/nedo/Documents/angioai/annotation/images'


#define output directory for dataset

DATASET_DIR = '/Users/nedo/Documents/angioai/datasets/yolo-annotation'

#define extension for localisation classes
LOC_EXT = ".loc.txt"
#define extension for classification classes
CLASS_EXT = ".txt"

IMG_EXT = ".png"



#define training set percentage
TRAIN_SET_PERCENTAGE = 0.7
#define validation set percentage
VALID_SET_PERCENTAGE = 0.2
#define test set percentage
TEST_SET_PERCENTAGE = 0.1


# if output directory does not exist, create it
if not os.path.exists(DATASET_DIR):
    os.makedirs(DATASET_DIR)

#create lables and images directories in output directory if they dont exist already and create test, train  and valid subdirectories in every one of them
if not os.path.exists(DATASET_DIR + "/labels"):
    os.makedirs(DATASET_DIR + "/labels")
    os.makedirs(DATASET_DIR + "/labels/train")
    os.makedirs(DATASET_DIR + "/labels/valid")
    os.makedirs(DATASET_DIR + "/labels/test")

if not os.path.exists(DATASET_DIR + "/images"):
    os.makedirs(DATASET_DIR + "/images")
    os.makedirs(DATASET_DIR + "/images/train")
    os.makedirs(DATASET_DIR + "/images/valid")
    os.makedirs(DATASET_DIR + "/images/test")








#get all files with LOC_EXT extension from ANNOTATIONS_DIR directory and divide them into train, valid and test sets
#use percentages defined in TRAIN_SET_PERCENTAGE, VALID_SET_PERCENTAGE and TEST_SET_PERCENTAGE variables
#count number of files in ANNOTATIONS_DIR directory with LOC_EXT extension
count_loc = 0
for file in os.listdir(ANNOTATIONS_DIR):
    #count all files with LOC_EXT extension
    if file.endswith(LOC_EXT):
        count_loc += 1

#define number of files in train, valid and test sets
train_loc = int(count_loc * TRAIN_SET_PERCENTAGE)
valid_loc = int(count_loc * VALID_SET_PERCENTAGE)
test_loc = int(count_loc * TEST_SET_PERCENTAGE)

#go over all files in ANNOTATIONS_DIR directory with LOC_EXT extension and copy them to train, valid and test sets directories changing LOC_EXT extension to .txt
i = 0
for file in os.listdir(ANNOTATIONS_DIR):
    #if file does not have LOC_EXT extension, skip it
    if not file.endswith(LOC_EXT):
        continue
    #defined if we are in trani valid or test directory based on if i is less than train_loc, valid_loc or test_loc
    if i < train_loc:
        set = "train"
    elif i < train_loc + valid_loc:
        set = "valid"
    else:
        set = "test"


    #get te filename
    filename = os.fsdecode(file)

    #replace the LOC_EXT extension with .txt extension
    filename_txt = filename.replace(LOC_EXT, ".txt")

    #get the image filename which is the same as the annotation filename but with IMG_EXT extension
    image_filename = filename_txt.replace(".txt", IMG_EXT)

    #check if image with the same name as the annotation file exists in IMAGES_DIR directory (strip LOC_EXT extension from file name and add IMG_EXT extension)
    if not os.path.exists(IMAGES_DIR + "/" + image_filename):
        print("Image " + image_filename + " does not exist")
        continue
    else:
        #copy file to train, valid or test directory and change extension to .txt
        shutil.copyfile(ANNOTATIONS_DIR + "/" + filename, DATASET_DIR + "/labels/" + set + "/" + filename_txt)
        #copy image to train, valid or test directory
        shutil.copyfile(IMAGES_DIR + "/" + image_filename, DATASET_DIR + "/images/" + set + "/" + image_filename)
        i += 1

#print summary how many files were copied to train, valid and test sets
print("Number of localization files in train set: " + str(train_loc))
print("Number of localization files in valid set: " + str(valid_loc))
print("Number of localization files in test set: " + str(test_loc))
#print total number of files exported
print("Total number of localization files exported: " + str(train_loc + valid_loc + test_loc))



    
    
        




