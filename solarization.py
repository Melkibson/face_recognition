import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('training-data/dorian/dorian.jpg')
img.savefig('gray.png')

lum_img = img[:, :, 0]
lum_img.savefig('lum_img.png')
