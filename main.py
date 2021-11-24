import pygame
pygame.init()
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
PIXEL_SIZE = 50
FPS = 60
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

class Pixel(pygame.Surface):
    def __init__(self, x, y, color):
        super().__init__((PIXEL_SIZE, PIXEL_SIZE))
        self.x = x
        self.y = y
        self.color = color
        self.fill(self.color)
    def show(self):
        window.blit(self, (self.x, self.y))

level_map = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,0,1,0,1,1,0,1,0,1,0],
    [0,1,0,1,0,0,0,0,1,0,1,0],
    [0,1,0,1,0,1,1,0,1,0,1,0],
    [0,1,0,1,0,0,0,0,1,0,1,0],
    [0,0,0,0,0,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,1,0,0,0,0,0],
    [0,1,0,1,0,0,0,0,1,0,1,0],
    [0,1,0,1,0,1,1,0,1,0,1,0],
    [0,1,0,1,0,0,0,0,1,0,1,0],
    [0,1,0,1,0,1,1,0,1,0,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0]
]

walls = []

def show_level():
    p_y = 0
    for line in level_map:
        p_x = 0
        for pixel in line:
            if pixel == 0:
                pass
            elif pixel == 1:
                wall = Pixel(p_x, p_y, (200, 0, 0))
                walls.append(wall)
            p_x += PIXEL_SIZE
        p_y += PIXEL_SIZE
show_level()


game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    
    for wall in walls:
        wall.show()

    pygame.display.update()
    clock.tick(FPS)