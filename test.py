import pygame
import pygame.camera

DEVICE = '/dev/video0'
SIZE = (640, 480)
FILENAME = 'capture.png'


def camstream():
    pygame.init()
    pygame.camera.init()
    display = pygame.display.set_mode(SIZE, 0)
    camera = pygame.camera.Camera(DEVICE, SIZE, "RGB")
    camera.start()
    screen = pygame.surface.Surface(SIZE, 0, display)
    capture = True
    while capture:
        screen = camera.get_image(screen)
        display.blit(screen, (0, 0))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                capture = False
                return
            elif event.type == pygame.KEYDOWN:
                # If pressed key is ESC quit program
                if event.key == pygame.K_ESCAPE or pygame.K_q:
                    capture = False
    camera.stop()
    pygame.quit()
    return


if __name__ == '__main__':
    camstream()
