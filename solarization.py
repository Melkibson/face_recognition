from PIL import Image, ImageOps

img = Image.open("training-data/dorian/dorian.jpg")
gray = ImageOps.grayscale(img)
solarize = ImageOps.solarize(gray, threshold=128)

gray.save("gray.jpg")
solarize.save("solarize.jpg")
