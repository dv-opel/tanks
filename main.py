import pygame
pygame.init()
import os
from random import randint

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

music_start = pygame.mixer.Sound(file_path("audio/start.ogg"))
music_game_over = pygame.mixer.Sound(file_path("audio/game_over.ogg"))
music_shot = pygame.mixer.Sound(file_path("audio/shot.ogg"))
music_shot_tank = pygame.mixer.Sound(file_path("audio/shot_tank.ogg"))
music_shot_wall = pygame.mixer.Sound(file_path("audio/shot_wall.ogg"))
music_tank_go = pygame.mixer.Sound(file_path("audio/tank_go.ogg"))
music_tank_start = pygame.mixer.Sound(file_path("audio/tank_star.ogg"))
music_start.play()

class Pixel(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, pic_name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(file_path(pic_name)).convert_alpha()        
    def show_image(self):
        window.blit(self.image, self.rect)

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way, w = PIXEL_SIZE, h = PIXEL_SIZE):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.image_w = pygame.image.load(pic_name_w).convert_alpha()
        self.image_d = pygame.image.load(pic_name_d).convert_alpha()
        self.image_s = pygame.image.load(pic_name_s).convert_alpha()
        self.image_a = pygame.image.load(pic_name_a).convert_alpha()
        self.way = way
        if way == "w":
            self.image = self.image_w
        elif way == "d":
            self.image = self.image_d
        elif way == "s":
            self.image = self.image_s
        elif way == "a":
            self.image = self.image_a    
        self.speed = speed
        self.can_move_w = True
        self.can_move_d = True
        self.can_move_s = True
        self.can_move_a = True
    def show(self):
        window.blit(self.image, self.rect)
    def can_move(self):
        c = pygame.sprite.spritecollide(self, walls_show, False)
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
    def shoot(self):
        if self.way == "w":
            bullet = Bullet(self.rect.centerx - 5, self.rect.top - 7, "images/bullet_w.png", "images/bullet_d.png", "images/bullet_s.png", "images/bullet_a.png", 3, self.way, 10, 10)
        elif self.way == "d":
            bullet = Bullet(self.rect.right, self.rect.centery - 5, "images/bullet_w.png", "images/bullet_d.png", "images/bullet_s.png", "images/bullet_a.png", 3, self.way, 10, 10)
        elif self.way == "s":
            bullet = Bullet(self.rect.centerx - 5, self.rect.bottom, "images/bullet_w.png", "images/bullet_d.png", "images/bullet_s.png", "images/bullet_a.png", 3, self.way, 10, 10)
        elif self.way == "a":
            bullet = Bullet(self.rect.left - 7, self.rect.centery - 5, "images/bullet_w.png", "images/bullet_d.png", "images/bullet_s.png", "images/bullet_a.png", 3, self.way, 10, 10)
        bullet.add(bullets)
        music_shot.play()

class Enemy(Tank):
    def __init__(self, x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way, w = PIXEL_SIZE, h = PIXEL_SIZE):
        super().__init__(x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way)
        self.shot_time = randint(100, 500)

    def update(self):
        self.shot_time -= 1
        if self.shot_time <= 0:
            self.shoot()
            self.shot_time = randint(100, 500)
                
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
            music_tank_go.play()
        elif keys[pygame.K_RIGHT] and self.rect.x < WINDOW_WIDTH - PIXEL_SIZE and self.can_move_d:
            if self.rect.y % PIXEL_SIZE >= 25:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_d
            self.way = "d"
            self.rect.x += self.speed
            music_tank_go.play()
        elif keys[pygame.K_UP] and self.rect.y > 0 and self.can_move_w:
            if self.rect.x % PIXEL_SIZE >= 25:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_w
            self.way = "w"
            self.rect.y -= self.speed
            music_tank_go.play()
        elif keys[pygame.K_DOWN] and self.rect.y < WINDOW_HEIGHT - PIXEL_SIZE and self.can_move_s:
            if self.rect.x % PIXEL_SIZE >= 25:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_s
            self.way = "s"
            self.rect.y += self.speed
            music_tank_go.play()

class Bullet(Tank):
    def update(self):
        global play
        if self.way == "w":
            self.rect.y -= self.speed
        elif self.way == "d":
            self.rect.x += self.speed
        elif self.way == "s":
            self.rect.y += self.speed
        elif self.way == "a":
            self.rect.x -= self.speed
        
        if self.rect.top <= 0 or self.rect.left <= 0 or self.rect.right >= WINDOW_WIDTH or self.rect.bottom >= WINDOW_HEIGHT:
            self.create_bullet_bam()
            self.kill()
            music_shot_wall.play()
        
        if pygame.sprite.spritecollide(self, walls_brick, True):
            self.create_bullet_bam()
            self.kill()
            music_shot_wall.play()
        
        if pygame.sprite.spritecollide(self, walls_titan, False):
            self.create_bullet_bam()
            self.kill()
            music_shot_wall.play()

        if pygame.sprite.spritecollide(self, tanks, True):
            self.create_bullet_bam()
            self.kill()
            music_shot_tank.play()

        if pygame.sprite.collide_rect(self, player):
            self.create_bullet_bam()
            self.kill()
            music_game_over.play()
            tanks.empty()
            play = False
        

    def create_bullet_bam(self):
        if self.way == "w":
            bullet_bam = BulletBam(self.rect.centerx - 20, self.rect.top - 20, 40, 40, file_path("images/bullet_bam.png"))
        elif self.way == "d":
            bullet_bam = BulletBam(self.rect.right - 20, self.rect.centery - 20, 40, 40, file_path("images/bullet_bam.png"))
        elif self.way == "s":
            bullet_bam = BulletBam(self.rect.centerx - 20, self.rect.bottom - 20, 40, 40, file_path("images/bullet_bam.png"))
        elif self.way == "a":
            bullet_bam = BulletBam(self.rect.left - 20, self.rect.centery - 20, 40, 40, file_path("images/bullet_bam.png"))
        bullet_bams.add(bullet_bam)

class BulletBam(Pixel):
    def __init__(self, x, y, width, height, pic_name):
        super().__init__(x, y, width, height, pic_name)
        self.timer = 3
    def update(self):
        if self.timer >= 0:
            self.show_image()
            self.timer -= 1
        else:
            self.kill()

level_map = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,1,3,1,0,1,1,0,1,3,1,0],
    [0,1,2,1,0,3,3,0,1,2,1,0],
    [0,1,0,1,0,1,1,0,1,0,1,0],
    [0,4,4,4,0,0,0,0,4,4,4,0],
    [0,0,0,0,0,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,1,0,0,0,0,0],
    [0,1,0,1,0,0,0,0,1,0,1,0],
    [0,1,0,1,0,1,1,0,1,0,1,0],
    [0,1,2,1,0,3,3,0,1,2,1,0],
    [0,1,3,1,0,1,1,0,1,3,1,0],
    [0,0,0,0,0,0,0,0,0,0,0,0]
]

def show_level():
    p_y = 0
    for line in level_map:
        p_x = 0
        for pixel in line:
            if pixel == 0:
                pass
            elif pixel == 1:
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "images/wall.png")
                walls_show.add(wall)
                walls_brick.add(wall)
            elif pixel == 2:
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "images/wall-titan.jpg")
                walls_show.add(wall)
                walls_titan.add(wall)
            elif pixel == 3:
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "images/wall-green.png")
                walls_show_green.add(wall)
            elif pixel == 4:
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "images/wall-water.jpg")
                walls_show.add(wall)
                walls_water.add(wall)
            p_x += PIXEL_SIZE
        p_y += PIXEL_SIZE

def create_enemys():
    tank1 = Enemy(0, 0, file_path("images/tanks/enemy1-w.png"), file_path("images/tanks/enemy1-d.png"), file_path("images/tanks/enemy1-s.png"), file_path("images/tanks/enemy1-a.png"), 2, "s")
    tank2 = Enemy(WINDOW_WIDTH - PIXEL_SIZE, 0, file_path("images/tanks/enemy2-w.png"), file_path("images/tanks/enemy2-d.png"), file_path("images/tanks/enemy2-s.png"), file_path("images/tanks/enemy2-a.png"), 2, "s")
    tank3 = Enemy(0, 150, file_path("images/tanks/enemy3-w.png"), file_path("images/tanks/enemy3-d.png"), file_path("images/tanks/enemy3-s.png"), file_path("images/tanks/enemy3-a.png"), 2, "s")
    tank4 = Enemy(WINDOW_WIDTH - PIXEL_SIZE, 150, file_path("images/tanks/enemy4-w.png"), file_path("images/tanks/enemy4-d.png"), file_path("images/tanks/enemy4-s.png"), file_path("images/tanks/enemy4-a.png"), 2, "s")
    tanks.add(tank1)
    tanks.add(tank2)
    tanks.add(tank3)
    tanks.add(tank4)

player = Player(200, 550, file_path("images/tanks/tank-yellow-w.png"), file_path("images/tanks/tank-yellow-d.png"), file_path("images/tanks/tank-yellow-s.png"), file_path("images/tanks/tank-yellow-a.png"), 2, "w")

walls_show = pygame.sprite.Group()
walls_show_green = pygame.sprite.Group()
walls_brick = pygame.sprite.Group()
walls_titan = pygame.sprite.Group()
walls_water = pygame.sprite.Group()

bullets = pygame.sprite.Group()
bullet_bams = pygame.sprite.Group()

tanks = pygame.sprite.Group()
create_enemys()
#print(walls.sprites()[0])
#print(player.rect.right)

show_level()
game = True
play = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and play:
                player.shoot()
            if event.key == pygame.K_r:
                player.rect.x = 200
                player.rect.y = 550
                create_enemys()
                play = True

    if play:
        window.fill((0, 0, 0))
        
        walls_show.draw(window)

        tanks.draw(window)
        tanks.update()

        player.can_move()
        player.update()
        player.show()

        bullets.update()
        bullets.draw(window)
        bullet_bams.update()

        walls_show_green.draw(window)

    pygame.display.update()
    clock.tick(FPS)