import zipfile

from PIL import Image, ImageDraw
import pytesseract
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt
np.set_printoptions(threshold=np.inf)
# loading the face detection classifier


# the rest is up to you!

        
        
        
def checkiftextExists(text,img):
    txt_str = pytesseract.image_to_string(img)
    if(text in txt_str):
        return True
    else:
        return False
        
def detectFaces(img):
    face_cascade = cv.CascadeClassifier('readonly/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img,1.35)
    return faces

def cropimages(img, face):
    crop_img = img[face[1]:face[1]+face[3], face[0]:face[0]+face[2]]
    image = Image.fromarray(crop_img)
    return crop_img
    
def getImageData(data):
    image = data.convert('L')
    image = np.array(image)
    
    return image
    
    
def getImages(filename, text):  
    with zipfile.ZipFile(filename, "r") as f:
        for info in f.infolist():
            ifile = f.open(info)
            img = Image.open(ifile)
            img1 = getImageData(img)
            img_arr = []
            if(checkiftextExists(text,img)):
                print("Results found in file {}".format(ifile.name))
                faces = detectFaces(img1)
                if len(faces) > 0:
                    for face in faces:
                        img_arr.append(cropimages(img1, face))
                    first_image=Image.fromarray(img_arr[0])
                    contact_sheet=Image.new(first_image.mode, (194*5, 194*2))
                    x=0
                    y=0
                    for img in img_arr:
                        img = Image.fromarray(img) 
                        newsize = (194, 194)
                        img = img.resize(newsize)
                        contact_sheet.paste(img, (x, y) )
                        if x+img.width == 194*5:
                            x=0
                            y=y+img.height
                        else:
                            x=x+img.width
                    display(contact_sheet)
                else:
                    print("But there are no faces in file {}".format(ifile.name))
            
getImages("readonly/small_img.zip","Christopher")
getImages("readonly/images.zip","Mark")
