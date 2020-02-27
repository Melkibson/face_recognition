import test
import test.camera
from test.locals import *

DEVICE = '/dev/video0'
SIZE = (640, 480)
FILENAME = 'capture.png'


def camstream():
    test.init()
    test.camera.init()
    display = test.display.set_mode(SIZE, 0)
    camera = test.camera.Camera(DEVICE, SIZE)
    camera.start()
    screen = test.surface.Surface(SIZE, 0, display)
    capture = True
    while capture:
        screen = camera.get_image(screen)
        display.blit(screen, (0, 0))
        test.display.flip()
        for event in test.event.get():
            if event.type == QUIT:
                capture = False
            elif event.type == KEYDOWN and event.key == K_s:
                test.image.save(screen, FILENAME)
    camera.stop()
    test.quit()
    return


if __name__ == '__main__':
    camstream()
