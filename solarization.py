from PIL import Image, ImageOps

img = Image.open("training-data/dorian/dorian.jpg")
gray = ImageOps.grayscale(img)
equalize = ImageOps.equalize(gray, mask=None)
solarize = ImageOps.solarize(equalize, threshold=128)

gray.save("gray.jpg")
equalize.save("equalize.jpg")
solarize.save("solarize.jpg")
