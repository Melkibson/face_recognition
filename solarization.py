from PIL import Image, ImageOps

i = 0

while not i == 11:
    i = i + 1

    i1 = Image.open("dorian10.jpg")
    i1 = ImageOps.grayscale(i1)
    i1 = ImageOps.solarize(i1, threshold=128)

    img = Image.open("dorian" + str(i) + ".jpg")
    gray = ImageOps.grayscale(img)
    solarize = ImageOps.solarize(gray, threshold=128)
    solarize.save("solarize" + str(i) + ".jpg")

    i2 = solarize
    assert i1.mode == i2.mode, "Different kinds of images."
    assert i1.size == i2.size, "Different sizes."

    pairs = zip(i1.getdata(), i2.getdata())
    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = i1.size[0] * i1.size[1] * 3
    print("Difference (percentage) pour " + "dorian" + str(i) + ".jpg" + " :", dif)
