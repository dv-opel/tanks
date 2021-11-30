import pygame
pygame.init()
import os

def image_path(im_name):
    return os.path.join(os.path.abspath(__file__ + "/.."), im_name)

os.environ['SDL_VIDEO_CENTERED'] = '1'
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
PIXEL_SIZE = 50
FPS = 60
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
    def __init__(self, x, y, pic_name, speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, PIXEL_SIZE, PIXEL_SIZE)
        self.image = pygame.image.load(pic_name)
        self.speed = speed
    def show(self):
        window.blit(self.image, self.rect)
    def canMove(self, wall):
        if self.rect.colliderect(wall.rect):
            return False
        else:
            return True

class Player(gameSprite):
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            if self.rect.y % PIXEL_SIZE >= 25:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE
            self.image = pygame.image.load(image_path("images/tank-yellow-a.png"))
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.x < WINDOW_WIDTH - PIXEL_SIZE:
            if self.rect.y % PIXEL_SIZE >= 25:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE
            self.image = pygame.image.load(image_path("images/tank-yellow-d.png"))
            self.rect.x += self.speed
        elif keys[pygame.K_UP] and self.rect.y > 0:
            if self.rect.x % PIXEL_SIZE >= 25:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE
            self.image = pygame.image.load(image_path("images/tank-yellow-w.png"))
            self.rect.y -= self.speed
        elif keys[pygame.K_DOWN] and self.rect.y < WINDOW_HEIGHT - PIXEL_SIZE:
            if self.rect.x % PIXEL_SIZE >= 25:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE
            self.image = pygame.image.load(image_path("images/tank-yellow-s.png"))
            self.rect.y += self.speed
        self.show()

player = Player(200, 550, image_path("images/tank-yellow-w.png"), 2)

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
                wall = Pixel(p_x, p_y, (200, 0, 0), image_path("images/wall.png"))
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