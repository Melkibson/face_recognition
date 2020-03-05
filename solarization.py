from PIL import Image, ImageOps

img = Image.open("training-data/dorian/dorian.jpg")
gray = ImageOps.grayscale(img)
solarize = ImageOps.solarize(gray, threshold=128)

gray.save("gray.jpg")
solarize.save("solarize.jpg")

i1 = Image.open("gray.jpg")
i2 = Image.open("solarize.jpg")
assert i1.mode == i2.mode, "Different kinds of images."
assert i1.size == i2.size, "Different sizes."

pairs = zip(i1.getdata(), i2.getdata())
if len(i1.getbands()) == 1:
    # for gray-scale jpegs
    dif = sum(abs(p1 - p2) for p1, p2 in pairs)
else:
    dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

ncomponents = i1.size[0] * i1.size[1] * 3
print("Difference (percentage):", (dif / 255.0 * 100) / ncomponents)