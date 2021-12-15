import pygame
pygame.init()
import os
from random import randint, choice

def tank_path(im_name):
    return os.path.join(os.path.abspath(__file__ + "/.."), "images", "tanks", im_name)
def image_path(im_name):
    return os.path.join(os.path.abspath(__file__ + "/.."), "images", im_name)
def audio_path(im_name):
    return os.path.join(os.path.abspath(__file__ + "/.."), "audio", im_name)

os.environ['SDL_VIDEO_CENTERED'] = '1'
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600
PIXEL_SIZE = 50
FPS = 60
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Tanks")
pygame.display.set_icon(pygame.image.load(image_path("wall_icon.bmp")))
clock = pygame.time.Clock()

music_start = pygame.mixer.Sound(audio_path("start.ogg"))
music_game_over = pygame.mixer.Sound(audio_path("game_over.ogg"))
music_shot = pygame.mixer.Sound(audio_path("shot.ogg"))
music_shot_tank = pygame.mixer.Sound(audio_path("shot_tank.ogg"))
music_shot_wall = pygame.mixer.Sound(audio_path("shot_wall.ogg"))
music_tank_go = pygame.mixer.Sound(audio_path("tank_go.ogg"))
music_tank_start = pygame.mixer.Sound(audio_path("tank_star.ogg"))
music_start.play()

pygame.time.set_timer(pygame.USEREVENT, 10000)

class Pixel(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, pic_name):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.image.load(image_path(pic_name)).convert_alpha()        
    def show_image(self):
        window.blit(self.image, self.rect)

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way, w = PIXEL_SIZE, h = PIXEL_SIZE):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        self.image_w = pygame.image.load(tank_path(pic_name_w)).convert_alpha()
        self.image_d = pygame.image.load(tank_path(pic_name_d)).convert_alpha()
        self.image_s = pygame.image.load(tank_path(pic_name_s)).convert_alpha()
        self.image_a = pygame.image.load(tank_path(pic_name_a)).convert_alpha()
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
        self.bullet_speed = 3
        self.can_move_w = True
        self.can_move_d = True
        self.can_move_s = True
        self.can_move_a = True
    def show(self):
        window.blit(self.image, self.rect)
    def collide_sprites_draw_collide(self):
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

    def collide_tanks(self):
        for tank in tanks:
            if self is tank:
                pass
            elif pygame.sprite.collide_rect(self, tank):
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
            #music_tank_go.play()
    def move_d(self):
        if self.rect.x < WINDOW_WIDTH - PIXEL_SIZE and self.can_move_d:
            if self.rect.y % PIXEL_SIZE >= 25:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_d
            self.way = "d"
            self.rect.x += self.speed
            #music_tank_go.play()
    def move_s(self):
        if self.rect.y < WINDOW_HEIGHT - PIXEL_SIZE and self.can_move_s:
            if self.rect.x % PIXEL_SIZE >= 25:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.x = self.rect.x // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_s
            self.way = "s"
            self.rect.y += self.speed
            #music_tank_go.play()
    def move_a(self):
        if self.rect.x > 0 and self.can_move_a:
            if self.rect.y % PIXEL_SIZE >= 25:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE + PIXEL_SIZE
            else:
                self.rect.y = self.rect.y // PIXEL_SIZE * PIXEL_SIZE
            self.image = self.image_a
            self.way = "a"
            self.rect.x -= self.speed
            #music_tank_go.play()
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
            bullet = Bullet(self.rect.centerx - 5, self.rect.top - 10, "bullet_w.png", "bullet_d.png", "bullet_s.png", "bullet_a.png", self.bullet_speed, self.way, 10, 10)
        elif self.way == "d":
            bullet = Bullet(self.rect.right, self.rect.centery - 5, "bullet_w.png", "bullet_d.png", "bullet_s.png", "bullet_a.png", self.bullet_speed, self.way, 10, 10)
        elif self.way == "s":
            bullet = Bullet(self.rect.centerx - 5, self.rect.bottom, "bullet_w.png", "bullet_d.png", "bullet_s.png", "bullet_a.png", self.bullet_speed, self.way, 10, 10)
        elif self.way == "a":
            bullet = Bullet(self.rect.left - 10, self.rect.centery - 5, "bullet_w.png", "bullet_d.png", "bullet_s.png", "bullet_a.png", self.bullet_speed, self.way, 10, 10)
        if isinstance(self, Player):
            bullet.add(bullets_player)
        elif isinstance(self, Enemy):
            bullet.add(bullets_enemys)
        music_shot.play()
        bullet.add(bullets)

class Enemy(Tank):
    def __init__(self, x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way, w = PIXEL_SIZE, h = PIXEL_SIZE):
        super().__init__(x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way)
        self.shot_time = randint(100, 250)
        self.add(tanks)
        self.move_time = randint(60, 150)

    def update(self):
        self.shot_time -= 1
        if self.shot_time <= 0:
            self.shoot()
            self.shot_time = randint(100, 250)
    
        self.move_time -= 1
        if self.move_time <= 0 or not self.collide_sprites_draw_collide():
            self.way = choice(["w", "d", "s", "a"])
            self.move_time = randint(60, 150)
        self.move_enemy()
        #self.collide_sprites_draw_collide()
        #self.collide_tanks()
        
class Player(Tank):
    def __init__(self, x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way, w = PIXEL_SIZE, h = PIXEL_SIZE):
        super().__init__(x, y, pic_name_w, pic_name_d, pic_name_s, pic_name_a, speed, way)
        self.bullets_limit = 1
        self.level = 1
    def change_images(self, pic_w, pic_d, pic_s, pic_a):
        self.image_w = pygame.image.load(tank_path(pic_w)).convert_alpha()
        self.image_d = pygame.image.load(tank_path(pic_d)).convert_alpha()
        self.image_s = pygame.image.load(tank_path(pic_s)).convert_alpha()
        self.image_a = pygame.image.load(tank_path(pic_a)).convert_alpha()
        if self.way == "w":
            self.image = self.image_w
        elif self.way == "d":
            self.image = self.image_d
        elif self.way == "s":
            self.image = self.image_s
        elif self.way == "a":
            self.image = self.image_a
    def change_level(self):
        if self.level == 1:
            self.change_images("tank-yellow-1-w.png", "tank-yellow-1-d.png", "tank-yellow-1-s.png", "tank-yellow-1-a.png")
            self.bullets_limit = 1
            self.bullet_speed = 3
        elif self.level == 2:
            self.change_images("tank-yellow-2-w.png", "tank-yellow-2-d.png", "tank-yellow-2-s.png", "tank-yellow-2-a.png")
            self.bullets_limit = 1
            self.bullet_speed = 5
        elif self.level == 3:
            self.change_images("tank-yellow-3-w.png", "tank-yellow-3-d.png", "tank-yellow-3-s.png", "tank-yellow-3-a.png")
            self.bullets_limit = 2
            self.bullet_speed = 5
        elif self.level == 4:
            self.change_images("tank-yellow-4-w.png", "tank-yellow-4-d.png", "tank-yellow-4-s.png", "tank-yellow-4-a.png")   
            self.bullets_limit = 2
            self.bullet_speed = 7
    def collide_time_pixel(self):
        if pygame.sprite.spritecollide(self, stars, True):
            self.level += 1
            self.change_level()

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
        self.collide_sprites_draw_collide()
        self.collide_time_pixel()

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
            time_pixel = Time_pixel(self.rect.centerx - 20, self.rect.top - 20, 40, 40, "bullet_bam.png", 100, False)
        elif self.way == "d":
            time_pixel = Time_pixel(self.rect.right - 20, self.rect.centery - 20, 40, 40, "bullet_bam.png", 100, False)
        elif self.way == "s":
            time_pixel = Time_pixel(self.rect.centerx - 20, self.rect.bottom - 20, 40, 40, "bullet_bam.png", 100, False)
        elif self.way == "a":
            time_pixel = Time_pixel(self.rect.left - 20, self.rect.centery - 20, 40, 40, "bullet_bam.png", 100, False)
        time_pixels.add(time_pixel)

class Time_pixel(Pixel):
    def __init__(self, x, y, width, height, pic_name, time_to_show, need_create_tank):
        super().__init__(x, y, width, height, pic_name)
        self.start_time = pygame.time.get_ticks()
        self.finish_time = 0
        self.time_to_show = time_to_show
        self.need_create_tank = need_create_tank
    def update(self):
        self.finish_time = pygame.time.get_ticks()
        if self.finish_time - self.start_time < self.time_to_show:
            self.show_image()
        else:
            self.kill()
            if self.need_create_tank:
                tank = Enemy(self.rect.x, self.rect.y, "enemy1-w.png", "enemy1-d.png", "enemy1-s.png", "enemy1-a.png", 2, "s")


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
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "wall.png")
                sprites_draw_collide.add(wall)
                walls_brick.add(wall)
            elif pixel == 2:
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "wall-titan.jpg")
                sprites_draw_collide.add(wall)
                walls_titan.add(wall)
            elif pixel == 3:
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "wall-green.png")
                walls_show_green.add(wall)
            elif pixel == 4:
                wall = Pixel(p_x, p_y, PIXEL_SIZE, PIXEL_SIZE, "wall-water.jpg")
                sprites_draw_collide.add(wall)
                walls_water.add(wall)
            p_x += PIXEL_SIZE
        p_y += PIXEL_SIZE

def create_time_pixel():
    x = randint(0, 22)
    y = randint(0, 22)
    time_pixel = Time_pixel(PIXEL_SIZE/2 * x, PIXEL_SIZE/2 * y, PIXEL_SIZE, PIXEL_SIZE, "star.png", 5000, False)
    stars.add(time_pixel)

start_enemy_positions = [
    pygame.Rect(0, 0, PIXEL_SIZE, PIXEL_SIZE),
    pygame.Rect(WINDOW_WIDTH - PIXEL_SIZE, 0, PIXEL_SIZE, PIXEL_SIZE),
    pygame.Rect(300, 0, PIXEL_SIZE, PIXEL_SIZE)
] 

def can_create(rect):
    res = True
    for tank in tanks.sprites():
        if tank.rect.colliderect(rect):
            res = False
    for star_tank in star_tanks.sprites():
        if star_tank.rect.colliderect(rect):
            res = False
    if player.rect.colliderect(rect):
        res = False
    return res

def create_enemys():
    if len(tanks.sprites()) + len(star_tanks.sprites()) < 3:
        start_enemy_position = choice(start_enemy_positions)
        if can_create(start_enemy_position):
            star_tank = Time_pixel(start_enemy_position.x, start_enemy_position.y, PIXEL_SIZE, PIXEL_SIZE, "star_tank.png", 1000, True)
            star_tank.add(star_tanks)
            

    '''
    start_ticks = pygame.time.get_ticks()
    seconds = (pygame.time.get_ticks() - start_ticks) / 1000 
    if seconds > 4:
    '''

player = Player(200, 550, "tank-yellow-1-w.png", "tank-yellow-1-d.png", "tank-yellow-1-s.png", "tank-yellow-1-a.png", 2, "w")
star_tanks = pygame.sprite.Group()
tanks = pygame.sprite.Group()

walls_show_green = pygame.sprite.Group()
walls_brick = pygame.sprite.Group()
walls_titan = pygame.sprite.Group()
walls_water = pygame.sprite.Group()

bullets = pygame.sprite.Group()
bullets_player = pygame.sprite.Group()
bullets_enemys = pygame.sprite.Group()

time_pixels = pygame.sprite.Group()
sprites_draw_collide = pygame.sprite.Group()

stars = pygame.sprite.Group()


#print(walls.sprites()[0])
#print(player.rect.right)

show_level()
game = True
play = True
a = True
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.USEREVENT:
            create_time_pixel()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and play:
                if len(bullets_player.sprites()) < player.bullets_limit:
                    player.shoot()
                
            if event.key == pygame.K_r:
                player.rect.x = 200
                player.rect.y = 550
                play = True
            if event.key == pygame.K_e:
                print(pygame.time.get_ticks())

    if play:
        window.fill((0, 0, 0))
        create_enemys()
        
        sprites_draw_collide.draw(window)

        player.update()
        player.show()

        tanks.draw(window)
        tanks.update()

        bullets.update()
        bullets.draw(window)

        star_tanks.update()
        time_pixels.update()
        stars.update()

        walls_show_green.draw(window)

    pygame.display.update()
    clock.tick(FPS)