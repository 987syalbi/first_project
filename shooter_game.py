from pygame import *
from random import randint
from time import sleep
display.set_caption("spicy X")
window = display.set_mode((700,500))
clock = time.Clock()
background = transform.scale(image.load('galaxy.jpg'),(700,500))
class GameSprite(sprite.Sprite):
    def __init__(self,playerImage,playerx,playery):
        super().__init__()
        self.image = transform.scale(image.load(playerImage),(80,120))
        self.rect = self.image.get_rect()
        self.rect.centerx = playerx
        self.rect.y = playery
class player(GameSprite):
    def update(self):
        keyPressed = key.get_pressed()
        if keyPressed[K_a] or keyPressed[K_LEFT]:
            self.rect.x -= 7.5
        if keyPressed[K_d] or keyPressed[K_RIGHT]:
            self.rect.x += 7.5
        window.blit(self.image,(self.rect.x,self.rect.y))
        if self.rect.centerx <= 0:
            self.rect.centerx = 699
        if self.rect.centerx >= 700:
            self.rect.centerx = 1
    def fire(self):
        bullet = Bullet('bullet.png',self.rect.centerx,self.rect.centery)
        bullets.add(bullet)
        mixer.music.load('fire.ogg')
        mixer.music.play()
        if not mixer.music.get_busy():
            mixer.music.load('space.ogg')
            mixer.music.play()
class Enemy(GameSprite):
    def update(self):
        global missed
        self.image = transform.scale(image.load('ufo.png'),(100,50))
        if self.rect.y <= 505:
            speed = randint(0,3)
            self.rect.y += speed
        else:
            self.rect.y = -10
            self.rect.x = randint(20,680)
            missed += 1
            for i in range(10):
                if self.rect.colliderect(ufo1) or self.rect.colliderect(ufo2) or self.rect.colliderect(ufo3) or self.rect.colliderect(ufo4) or self.rect.colliderect(ufo5):
                    self.rect.x = randint(20,680)
                    window.blit(self.image,(self.rect.x, self.rect.y))
        window.blit(self.image,(self.rect.x, self.rect.y))
class Bullet(GameSprite):
    def update(self):
        if self.rect.centery <= 0:
            self.kill()
        self.rect.centery -= 5
run = True
lose = False
win = False
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
missed = 0
rocket = player('rocket.png',350,350)
ufo1 = Enemy('ufo.png',randint(20,680),-10)
ufo2 = Enemy('ufo.png',randint(20,680),-10)
ufo3 = Enemy('ufo.png',randint(20,680),-10)
ufo4 = Enemy('ufo.png',randint(20,680),-10)
ufo5 = Enemy('ufo.png',randint(20,680),-10)
bullets = sprite.Group()
Enemys = sprite.Group()
Enemys.add(ufo1)
Enemys.add(ufo2)
Enemys.add(ufo3)
Enemys.add(ufo4)
Enemys.add(ufo5)
font.init()
font1 = font.Font(None,36)
bigFont = font.Font(None,80)
points = 0
while run:
    window.blit(background,(0,0))
    rocket.update()
    Enemys.draw(window)
    Enemys.update()
    bullets.draw(window)
    bullets.update()
    rocketCollide = sprite.spritecollide(rocket,Enemys,True)
    bulletCollide = sprite.groupcollide(Enemys,bullets,True,True)
    textMissed = font1.render('Missed: '+str(missed),1,(255, 255, 255))
    textpoints = font1.render('Points: '+str(points),1,(255, 255, 255))
    loseText = bigFont.render('you Lose!',1,(255,255,255))
    winText = bigFont.render('you win!',1,(255,255,255))
    window.blit(textMissed,(0,10))
    window.blit(textpoints,(0,40))
    keyPressed = key.get_pressed()
    for moai in bulletCollide:
        ufo = Enemy('ufo.png',randint(20,680),-10)
        Enemys.add(ufo)
        points += 1
    if keyPressed[K_e] or keyPressed[K_SPACE]:
        rocket.fire()
    if not mixer.music.get_busy():
        mixer.music.load('space.ogg')
        mixer.music.play()
    for moai in rocketCollide:
        run = False
        lose = True
    if points >= 50:
        run = False
        win = True
    if missed >= 10:
        run = False
        lose = True
    for e in event.get():
        if e.type == QUIT:
            run = False
    clock.tick(120)
    display.update()
if lose:
    mixer.music.stop()
    mixer.music.load('shut-down.ogg')
    mixer.music.play()
    window.blit(loseText,(225,200))
elif win:
    mixer.music.stop()
    mixer.music.load('you-win-perfect.ogg')
    mixer.music.play()
    window.blit(winText,(225,200))
textMissed = font1.render('Missed: '+str(missed),1,(255, 255, 255))
textpoints = font1.render('Points: '+str(points),1,(255, 255, 255))
window.blit(textMissed,(0,10))
window.blit(textpoints,(0,40))
while lose:
    window.blit(loseText,(225,200))
    textMissed = font1.render('Missed: '+str(missed),1,(255, 255, 255))
    textpoints = font1.render('Points: '+str(points),1,(255, 255, 255))
    window.blit(textMissed,(0,10))
    window.blit(textpoints,(0,40))
    for e in event.get():
        if e.type == QUIT:
            lose = False
    clock.tick(60)
    display.update()
while win:
    textMissed = font1.render('Missed: '+str(missed),1,(255, 255, 255))
    textpoints = font1.render('Points: '+str(50),1,(255, 255, 255))
    window.blit(textMissed,(0,10))
    window.blit(textpoints,(0,40))
    window.blit(winText,(225,200))
    for e in event.get():
        if e.type == QUIT:
            win = False
    clock.tick(60)
    display.update()