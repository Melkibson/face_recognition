import pygame

DEVICE = '/dev/video0'
SIZE = (1280, 720)
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
            if event.type == QUIT:
                camera.stop()
                pygame.quit()
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    camera.stop()
                    pygame.quit()


if __name__ == '__main__':
    camstream()
