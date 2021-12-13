import pygame
pygame.init()
import os
from random import randint, choice

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
        if pygame.sprite.spritecollide(self, sprites_draw_collide, False):
            if self.way == "w":
                self.can_move_w = False
                return False
            if self.way == "d":
                self.can_move_d = False
                return False
            if self.way == "s":
                self.can_move_s = False
                return False
            if self.way == "a":
                self.can_move_a = False
                return False
        else:
            self.can_move_w = True
            self.can_move_d = True
            self.can_move_s = True
            self.can_move_a = True
            return True
    def move_w(self):
        if self.rect.y > 0 and self.can_move_w:
            if self.rect.x % PIXEL_SIZE >= 25:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_w
            self.way = "w"
            self.rect.y -= self.speed
            music_tank_go.play()
    def move_d(self):
        if self.rect.x < WINDOW_WIDTH - PIXEL_SIZE and self.can_move_d:
            if self.rect.y % PIXEL_SIZE >= 25:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_d
            self.way = "d"
            self.rect.x += self.speed
            music_tank_go.play()
    def move_s(self):
        if self.rect.y < WINDOW_HEIGHT - PIXEL_SIZE and self.can_move_s:
            if self.rect.x % PIXEL_SIZE >= 25:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_s
            self.way = "s"
            self.rect.y += self.speed
            music_tank_go.play()
    def move_a(self):
        if self.rect.x > 0 and self.can_move_a:
            if self.rect.y % PIXEL_SIZE >= 25:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_a
            self.way = "a"
            self.rect.x -= self.speed
            music_tank_go.play()
    def move_enemy(self):
        if self.way == "a":
            self.move_a()
        elif self.way == "w":
            self.move_w()
        elif self.way == "d":
            self.move_d()
        elif self.way == "s":
            self.move_s()
    def shoot(self):
        if self.way == "w":
            bullet = Bullet(self.rect.centerx - 5, self.rect.top - 7, "images/bullet_w.png", "images/bullet_d.png", "images/bullet_s.png", "images/bullet_a.png", 3, self.way, 10, 10)
        elif self.way == "d":
            bullet = Bullet(self.rect.right, self.rect.centery - 5, "images/bullet_w.png", "images/bullet_d.png", "images/bullet_s.png", "images/bullet_a.png", 3, self.way, 10, 10)
        elif self.way == "s":
            bullet = Bullet(self.rect.centerx - 5, self.rect.bottom, "images/bullet_w.png", "images/bullet_d.png", "images/bullet_s.png", "images/bullet_a.png", 3, self.way, 10, 10)
        elif self.way == "a":
            bullet = Bullet(self.rect.left - 7, self.rect.centery - 5, "images/bullet_w.png", "images/bullet_d.png", "images/bullet_s.png", "images/bullet_a.png", 3, self.way, 10, 10)
        if isinstance(self, Player):
            bullet.add(bullets_player)
        elif isinstance(self, Enemy):
            bullet.add(bullets_enemys)
        music_shot.play()
        bullet.add(bullets)

class Enemy(Tank):
    def __init__(self, x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way, w = PIXEL_SIZE, h = PIXEL_SIZE):
        super().__init__(x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way)
        self.shot_time = randint(100, 300)
        self.add(tanks)
        self.move_time = randint(60, 150)

    def update(self):
        self.shot_time -= 1
        if self.shot_time <= 0:
            self.shoot()
            self.shot_time = randint(100, 300)
    
        self.move_time -= 1
        if self.move_time <= 0 or not self.can_move:
            self.way = choice(["w", "d", "s", "a"])
            self.move_time = randint(60, 150)
        self.move_enemy()
        self.can_move()
          
        
class Player(Tank):
    def __init__(self, x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way, w = PIXEL_SIZE, h = PIXEL_SIZE):
        super().__init__(x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way)
        self.bullets_limit = 1
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.move_a()
        elif keys[pygame.K_RIGHT]:
            self.move_d()
        elif keys[pygame.K_UP]:
            self.move_w()            
        elif keys[pygame.K_DOWN]:
            self.move_s()

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

        if self in bullets_player:
            if pygame.sprite.spritecollide(self, tanks, True):
                self.create_bullet_bam()
                self.kill()
                music_shot_tank.play()
            if pygame.sprite.spritecollide(self, bullets_enemys, True):
                self.kill()
        elif self in bullets_enemys:
            if pygame.sprite.spritecollide(self, tanks, False):
                self.kill()
        
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
                sprites_draw_collide.add(wall)
                walls_brick.add(wall)
            elif pixel == 2:
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "images/wall-titan.jpg")
                sprites_draw_collide.add(wall)
                walls_titan.add(wall)
            elif pixel == 3:
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "images/wall-green.png")
                walls_show_green.add(wall)
            elif pixel == 4:
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "images/wall-water.jpg")
                sprites_draw_collide.add(wall)
                walls_water.add(wall)
            p_x += PIXEL_SIZE
        p_y += PIXEL_SIZE

start_enemy_pos = True
start_enemy_pos1 = pygame.Rect(0, 0, PIXEL_SIZE, PIXEL_SIZE)
start_enemy_pos2 = pygame.Rect(WINDOW_WIDTH - PIXEL_SIZE, 0, PIXEL_SIZE, PIXEL_SIZE)

def can_create(rect):
    res = True
    for tank in tanks.sprites():
        if tank.rect.colliderect(rect):
            res = False
    if player.rect.colliderect(rect):
        res = False
    return res

def create_enemys():
    global start_enemy_pos
    if len(tanks.sprites()) < 2:
        if start_enemy_pos and can_create(start_enemy_pos1):
            tank = Enemy(0, 0, file_path("images/tanks/enemy1-w.png"), file_path("images/tanks/enemy1-d.png"), file_path("images/tanks/enemy1-s.png"), file_path("images/tanks/enemy1-a.png"), 2, "s")
            start_enemy_pos = False
        elif not start_enemy_pos and can_create(start_enemy_pos2):
            tank = Enemy(WINDOW_WIDTH - PIXEL_SIZE, 0, file_path("images/tanks/enemy2-w.png"), file_path("images/tanks/enemy2-d.png"), file_path("images/tanks/enemy2-s.png"), file_path("images/tanks/enemy2-a.png"), 2, "s")
            start_enemy_pos = True
        else:
            if can_create(start_enemy_pos1):
                tank = Enemy(0, 0, file_path("images/tanks/enemy1-w.png"), file_path("images/tanks/enemy1-d.png"), file_path("images/tanks/enemy1-s.png"), file_path("images/tanks/enemy1-a.png"), 2, "s")
                start_enemy_pos = False
            elif can_create(start_enemy_pos2):
                tank = Enemy(WINDOW_WIDTH - PIXEL_SIZE, 0, file_path("images/tanks/enemy2-w.png"), file_path("images/tanks/enemy2-d.png"), file_path("images/tanks/enemy2-s.png"), file_path("images/tanks/enemy2-a.png"), 2, "s")
                start_enemy_pos = True
    '''
    start_ticks = pygame.time.get_ticks()
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000 
    if seconds > 4:
    '''

player = Player(200, 550, file_path("images/tanks/tank-yellow-w.png"), file_path("images/tanks/tank-yellow-d.png"), file_path("images/tanks/tank-yellow-s.png"), file_path("images/tanks/tank-yellow-a.png"), 2, "w")

walls_show_green = pygame.sprite.Group()
walls_brick = pygame.sprite.Group()
walls_titan = pygame.sprite.Group()
walls_water = pygame.sprite.Group()

bullets = pygame.sprite.Group()
bullets_player = pygame.sprite.Group()
bullets_enemys = pygame.sprite.Group()
bullet_bams = pygame.sprite.Group()

tanks = pygame.sprite.Group()

sprites_draw_collide = pygame.sprite.Group()

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
                if len(bullets_player.sprites()) < player.bullets_limit:
                    player.shoot()
                
            if event.key == pygame.K_r:
                player.rect.x = 200
                player.rect.y = 550
                play = True
            if event.key == pygame.K_e:
                for t in tanks.sprites():
                    print(t.can_move_w)
                    print(t.can_move_d)
                    print(t.can_move_s)
                    print(t.can_move_a)
                    print("---")
                    print(pygame.sprite.spritecollide(t, sprites_draw_collide, False))
                    print("---")

    if play:
        window.fill((0, 0, 0))
        create_enemys()
        
        sprites_draw_collide.draw(window)

        tanks.draw(window)
        tanks.update()

        bullets.update()
        bullets.draw(window)
        bullet_bams.update()

        player.can_move()
        player.update()
        player.show()

        walls_show_green.draw(window)

    pygame.display.update()
    clock.tick(FPS)