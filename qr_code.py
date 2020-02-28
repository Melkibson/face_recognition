import pygame
import pygame.camera
import pyzbar.pyzbar as pyzbar

DEVICE = '/dev/video0'
SIZE = (640, 480)

user_code = 'http://google.fr'


def qr_code_reader():
    pygame.init()
    pygame.camera.init()
    display = pygame.display.set_mode(SIZE, 0)
    camera = pygame.camera.Camera(DEVICE, SIZE, "RGB")
    camera.start()
    capture = True
    while capture:
        screen = camera.get_image()
        display.blit(screen, (0, 0))
        pygame.display.flip()
        decodedObjects = pyzbar.decode(screen)

        for obj in decodedObjects:
            print("Type:", obj.type)
            print("Data: ", obj.data, "\n")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                capture = False
                return
            elif event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    capture = False
    camera.stop()
    pygame.quit()
    return


qr_code_reader()

