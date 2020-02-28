import pygame
from pygame import camera
from pygame.locals import *
import qrtools

pygame.init()
camera.init()

user_code = 'http://google.fr'


def qr_code_reader():
    camlist = camera.list_cameras()

    if camlist:
        cam = camera.Camera(camlist[0], (640, 480))
        image = cam.get_image()
        qr = qrtools.QR()
        qr.decode(image)
        s = qr.data
        print("The decoded QR code is: %s" % s)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print("pressed w")
            if event.key == pygame.K_s:
                print("pressed s")



qr_code_reader()
