import cv2
import numpy as np


solarization_const = 2 * np.pi / 255
look_up_table = np.ones((256, 1), dtype='uint8') * 0

for i in range(256):
    look_up_table[i][0] = np.abs(np.sin(i * solarization_const)) * 100

img_src = cv2.imread("training-data/dorian/dorian.jpg", 1)

img_sola = cv2.LUT(img_src, look_up_table)

cv2.imshow("Show SOLARIZATION Image", img_sola)
cv2.waitKey(0)
cv2.destroyAllWindows()
