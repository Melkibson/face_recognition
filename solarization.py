# Importing Image and ImageOps module from PIL package  
from PIL import Image, ImageOps
import time

# creating a image1 object  
im1 = Image.open(r"training-data/dorian/dorian.jpg")

# image segmentation  
# using threshold value = 130 
# applying solarize method  
im2 = ImageOps.solarize(im1, threshold=130)
time.sleep(3)

im1.show()
im2.show()
