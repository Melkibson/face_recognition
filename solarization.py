import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('training-data/dorian/dorian.jpg')
img.savefig('img.png')

lum_img = img[:, :, 0]
plt.imshow(lum_img, cmap="hot")
plt.savefig('lum_img.png')
