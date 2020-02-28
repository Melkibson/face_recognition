import pygame
import pygame.camera
import qrtools

DEVICE = '/dev/video0'

user_code = 'http://google.fr'


def qr_code_reader():
    pygame.init()
    pygame.camera.init()
    display = pygame.camera.Camera(DEVICE, (640, 480))
    cam = pygame.camera.Camera(DEVICE, (640, 480))
    cam.start()
    image = pygame.surface.Surface((640, 480), display )
    image = cam.get_image(image)
    capture = True
    while capture:
        qr = qrtools.QR()
        qr.decode(image)
        s = qr.data
    print("The decoded QR code is: %s" % s)

    cam.stop()
    pygame.quit()
    return


qr_code_reader()
