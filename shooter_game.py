#Создай собственный Шутер!
from time import time as timer
from pygame import *
from random import *
mixer.init()

font.init()
font2 = font.SysFont("Arial", 35)
font1 = font.SysFont("Arial", 35)
score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65,65) )
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, self.rect)

lost = 0 

score = 0

#class Enemy(GameSprite):
#    def update(self):
#        global lost
#        self.rect.y += self.speed
#        if self.rect.y > 500:
#            self.rect.y = 0
#            self.rect.x = randint(0,620)
#            lost += 1
        
class Enemy(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__(player_image, player_x, player_y, player_speed)
        self.direction = choice(["left", "right"])  # Начальное направление

    def update(self):
        global lost
        # Движение вниз
        self.rect.y += self.speed
        # Движение влево-вправо
        if self.direction == "right":
            self.rect.x += self.speed
            if self.rect.x > 620:  # Если достигает края, меняем направление
                self.direction = "left"
        elif self.direction == "left":
            self.rect.x -= self.speed
            if self.rect.x < 0:  # Если достигает другого края, меняем направление
                self.direction = "right"
        
        # Если враг уходит за нижний край, сбрасываем его
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0, 620)
            lost += 1

class Asteroid(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(0,620)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill
        

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 500 - 80:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx -30, self.rect.top, 15)
        bullets.add(bullet)


window = display.set_mode((700,500))
display.set_caption("Maze")

background = transform.scale(image.load("galaxy.jpg"), (700,500))

player = Player("rocket.png", 5, 420, 4)

asteroids = sprite.Group()
bullets = sprite.Group()
monsters = sprite.Group()
for i in range(5):
    monster = Enemy("ufo.png", randint(0,620), -40, randint(1,1) )
    monsters.add(monster)

for i in range(3):
    asteroides = Asteroid("asteroid.png", randint(0,620), -40, randint(1,2) )
    asteroids.add(asteroides)


num_fire = 0
rel_time = False



text_win = font1.render("you win!", True, (0,255,0))
window.blit(text_win, (350,250))

text_loose = font1.render("you lose!", True, (255,0,0))
window.blit(text_loose, (350,250))





finish = False


game = True
clock =time.Clock()

mixer.music.load("space.ogg")
mixer.music.play()
mixer.music.set_volume(0.1)


font.init()
font2 = font.SysFont("Arial", 30)

fire_sound = mixer.Sound("fire.ogg")


while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    player.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

        
            
            





    if not finish:
        window.blit(background, (0,0))
        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font2.render("Wait, reload...", True, (150,0,0))
                window.blit(reload, (250,400))
            else:
                num_fire = 0
                rel_time = False

        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()


        if lost > 2:
            finish = True
            window.blit(text_loose, (350,250))
        if sprite.spritecollide(player, monsters, False):
            finish = True
            window.blit(text_loose, (350,250))
        if sprite.spritecollide(player, asteroids, False):
            finish = True
            window.blit(text_loose, (350,250))
        if sprite.groupcollide(bullets, monsters, True,True):
            score += 1
            monster = Enemy("ufo.png", randint(0,620), -40, randint(1,1) )
            monsters.add(monster)
        if score > 9:
            finish = True
            window.blit(text_win, (350,250))
        

        text_lose = font2.render("Пропущено:"+str(lost), True, (255,255,255))
        window.blit(text_lose, (10,50))

        text_score = font2.render("Очков:"+str(score), True, (255,255,255))
        window.blit(text_score, (10,80))

        
    else:
        finish =False
        score = 0
        lost = 0
        for b in bullets:
            b.kill()
        for m in monsters:
            m.kill()
        time.delay(2000)
        for i in range(5):
            monster = Enemy('ufo.png', randint(0,620), -40, randint(1,1))
            monsters.add(monster)
            

    clock.tick(165)
    display.update()