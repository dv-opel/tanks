import pygame
pygame.init()
import os

def file_path(im_name):
    return os.path.join(os.path.abspath(__file__ + "/.."), im_name)

os.environ['SDL_VIDEO_CENTERED'] = '1'
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
PIXEL_SIZE = 50
FPS = 60
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tanks")
pygame.display.set_icon(pygame.image.load(file_path("images/wall_icon.bmp")))
clock = pygame.time.Clock()

class Pixel(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, pic_name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(file_path(pic_name)).convert()        
    def show_image(self):
        window.blit(self.image, self.rect)

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, PIXEL_SIZE, PIXEL_SIZE)
        self.image_w = pygame.image.load(pic_name_w).convert_alpha()
        self.image_d = pygame.image.load(pic_name_d).convert_alpha()
        self.image_s = pygame.image.load(pic_name_s).convert_alpha()
        self.image_a = pygame.image.load(pic_name_a).convert_alpha()
        self.image = self.image_w
        self.way = "w"
        self.speed = speed
        self.can_move_w = True
        self.can_move_d = True
        self.can_move_s = True
        self.can_move_a = True
    def show(self):
        window.blit(self.image, self.rect)
    def can_move(self):
        c = pygame.sprite.spritecollide(self, walls, False)
        if c:
            if self.way == "w":
                self.can_move_w = False
            if self.way == "d":
                self.can_move_d = False
            if self.way == "s":
                self.can_move_s = False
            if self.way == "a":
                self.can_move_a = False
        else:
            self.can_move_w = True
            self.can_move_d = True
            self.can_move_s = True
            self.can_move_a = True         
                

class Player(Tank):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.x > 0 and self.can_move_a:
            if self.rect.y % PIXEL_SIZE >= 25:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_a
            self.way = "a"
            self.rect.x -= self.speed
        elif keys[pygame.K_RIGHT] and self.rect.x < WINDOW_WIDTH - PIXEL_SIZE and self.can_move_d:
            if self.rect.y % PIXEL_SIZE >= 25:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_d
            self.way = "d"
            self.rect.x += self.speed
        elif keys[pygame.K_UP] and self.rect.y > 0 and self.can_move_w:
            if self.rect.x % PIXEL_SIZE >= 25:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_w
            self.way = "w"
            self.rect.y -= self.speed
        elif keys[pygame.K_DOWN] and self.rect.y < WINDOW_HEIGHT - PIXEL_SIZE and self.can_move_s:
            if self.rect.x % PIXEL_SIZE >= 25:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_s
            self.way = "s"
            self.rect.y += self.speed


player = Player(200, 550, file_path("images/tank-yellow-w.png"), file_path("images/tank-yellow-d.png"), file_path("images/tank-yellow-s.png"), file_path("images/tank-yellow-a.png"), 2)

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

walls = pygame.sprite.Group()

def show_level():
    p_y = 0
    for line in level_map:
        p_x = 0
        for pixel in line:
            if pixel == 0:
                pass
            elif pixel == 1:
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "images/wall.png")
                walls.add(wall)
            p_x += PIXEL_SIZE
        p_y += PIXEL_SIZE
show_level()

#print(walls.sprites()[0])
#print(player.rect.right)
game = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    window.fill((0, 0, 0))
    
    walls.draw(window)

    player.can_move()
    player.update()
    player.show()

    pygame.display.update()
    clock.tick(FPS)