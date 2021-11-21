import pygame
pygame.init()

WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
FPS = 60

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    pygame.display.update()
    clock.tick(FPS)

    #  ty