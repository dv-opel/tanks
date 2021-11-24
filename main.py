import pygame
pygame.init()
import os

os.environ['SDL_VIDEO_CENTERED'] = '1'
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
PIXEL_SIZE = 50
FPS = 10
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

class Pixel(pygame.Surface):
    def __init__(self, x, y, color, pic_name):
        super().__init__((PIXEL_SIZE, PIXEL_SIZE))
        self.x = x
        self.y = y
        self.color = color
        self.fill(self.color)
        self.image = pygame.image.load(pic_name)
    def show_color(self):
        window.blit(self, (self.x, self.y))
    def show_image(self):
        window.blit(self.image, (self.x, self.y))

class gameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, pic_name):
        super().__init__()
        self.rect = pygame.Rect(x, y, PIXEL_SIZE, PIXEL_SIZE)
        self.image = pygame.image.load(pic_name)
    def show(self):
        window.blit(self.image, self.rect)

class Player(gameSprite):
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= PIXEL_SIZE
        elif keys[pygame.K_RIGHT] and self.rect.x < WINDOW_WIDTH - PIXEL_SIZE:
            self.rect.x += PIXEL_SIZE
        elif keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= PIXEL_SIZE
        elif keys[pygame.K_DOWN] and self.rect.y < WINDOW_HEIGHT - PIXEL_SIZE:
            self.rect.y += PIXEL_SIZE
        self.show()

player = Player(200, 550, "images/tank-yellow-w.png")

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
                wall = Pixel(p_x, p_y, (200, 0, 0), "images/wall.png")
                walls.append(wall)
            p_x += PIXEL_SIZE
        p_y += PIXEL_SIZE
show_level()


game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    window.fill((0, 0, 0))
    
    for wall in walls:
        wall.show_image()

    player.move()

    pygame.display.update()
    clock.tick(FPS)