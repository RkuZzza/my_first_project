#Создай собственный Шутер!
from pygame import *
font.init()
font1 = font.SysFont("Arial", 36)
font2 = font.SysFont("Arial", 72)
font3 = font.SysFont("Arial", 54)

from time import time as timer
from random import randint

#создай окно игры
win_width = 900
win_height = 700
game_win = display.set_mode((win_width, win_height))
display.set_caption("Космический шутер")

#задай фон сцены
background = image.load("galaxy.jpg")
background = transform.scale(background, (win_width,win_height))
clock = time.Clock()
FPS = 60
lost = 0
score = 0
health = 3

#подключим музыку
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()
fire_sound = mixer.Sound("fire.ogg")

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))    
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y 
        self.size_x = size_x
        self.size_y = size_y
    def reset(self):
        game_win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        
        if keys[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x += self.speed
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 10, 25, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= win_height:
            self.rect.x = randint(5, win_width - 90)
            self.rect.y = -60
            self.speed = randint(1,4)
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.x = randint(5, win_width - 90)
            self.rect.y = -60
            self.speed = randint(1,4)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

#обработай событие «клик по кнопке "Закрыть окно"»
ship = Player("rocket.png", win_width // 2, win_height - 105, 80, 100, 10)
ufos = sprite.Group()
for i in range(1,6):
    ufo = Enemy("ufo.png", randint(5, win_width - 90), -60, 80, 40, randint(1,4))
    ufos.add(ufo)
bullets = sprite.Group()
asteroids = sprite.Group()
for i in range(3):
    asteroid = Asteroid("asteroid.png", randint(5, win_width - 90), -60, 50, 50, randint(1,4))
    asteroids.add(asteroid)

text_lose = font1.render("Пропущено: " 
                + str(lost), True, (255,255,255))
game_win.blit(text_lose, (10, 50))

text_win = font1.render("Сбито: " 
                + str(score), True, (255,255,255))
game_win.blit(text_win, (win_width - 140, 50))

finish = False
game = True

num_fire = 0
rel_time = False

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
    
                if num_fire >= 5:
                    rel_time = True
                    now_time = timer()

    if finish != True:
        game_win.blit(background, (0,0))
        ship.update()
        ship.reset()
        ufos.update()
        ufos.draw(game_win)
        bullets.update()
        bullets.draw(game_win)
        asteroids.update()
        asteroids.draw(game_win)

        collide_list = sprite.groupcollide(ufos, bullets, True, True)
        for c in collide_list:
            score += 1
            ufo = Enemy("ufo.png", randint(5, win_width - 90), -60, 80, 40, randint(1,4))
            ufos.add(ufo)

        if rel_time:
            current_time = timer()
            if current_time - now_time < 3:
                reload = font2.render("Ждите, перезагрузка...", 
                                            True, (255,255,255))
                game_win.blit(reload, (370, 500))
            else:
                num_fire = 0
                rel_time = False


        if lost >= 5 or sprite.spritecollide(ship, ufos, False):
            LOSER = font2.render("ТЫ ПРОИГРАЛ!", True, (180,0,0))
            game_win.blit(LOSER, (150, 300))
            finish = True

        if score >= 20:
            WINNER = font2.render("ТЫ ПОБЕДИЛ!", True, (0,180,0))
            game_win.blit(WINNER, (150, 300))
            finish = True

        if sprite.spritecollide(ship, asteroids, True):
            health -= 1
            if health < 1:
                LOSER = font2.render("ТЫ ПРОИГРАЛ!", True, (180,0,0))
                game_win.blit(LOSER, (150, 300))
                finish = True         
                
        text_lose = font1.render("Пропущено: " 
                + str(lost), True, (255,255,255))
        text_win = font1.render("Сбито: " 
                + str(score), True, (255,255,255))
        game_win.blit(text_lose, (10, 50))
        game_win.blit(text_win, (win_width - 140, 50))
        text_health = font3.render(str(health), True, (255,255,255))
        game_win.blit(text_health, (win_width // 2, 50))
        display.update()
    else:
        for b in bullets:
            b.kill()

        for u in ufos:
            u.kill()

        num_fire = 0
        lost = 0
        score = 0
        health = 3
        for i in range(1,6):
            ufo = Enemy("ufo.png", randint(5, win_width - 90), -60, 80, 40, randint(1,4))
            ufos.add(ufo)
        finish = False
        time.delay(3000)

    

    
    display.update()
    clock.tick(FPS)
