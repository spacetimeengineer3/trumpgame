import pygame
from pygame.locals import *
import random


pygame.init()

clock = pygame.time.Clock()


class Sans(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/sans.png").convert_alpha()
        self.rect = self.image.get_rect()


class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/meteor.png").convert_alpha()
        self.rect = self.image.get_rect()


class Trump(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/dtrump.png").convert_alpha()
        self.rect = self.image.get_rect()

def get_size(): #this will get the screen resolution via the appropriate OS commands and place it into two Variables called screenWidth and screenHeight
    pass

white = (255, 255, 255)
black = (  0,   0,   0)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)
icon = pygame.image.load("images/icon.png")
screenWidth = 1920
screenHeight = 1080
screenSize = [screenWidth, screenHeight]
screen = pygame.display.set_mode(screenSize, pygame.FULLSCREEN)
pygame.display.set_caption("Nightmare")
pygame.display.set_icon(icon)

trump = Trump()
trump.rect.x = 10
trump.rect.y = 10

sans = Sans()
sans.rect.x = 900
sans.rect.y = 900



allsprites = pygame.sprite.Group()
allsprites.add(sans)
allsprites.add(trump)
bullets = pygame.sprite.Group() 

movespeed = 20
    
x = 0

def check_keys(): 
    global sans
    global bullets
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT] and sans.rect.x + sans.rect.width < screenWidth:
        sans.rect.x += movespeed
    if keys[K_LEFT] and sans.rect.x > 5:
        sans.rect.x -= movespeed
    if keys[K_UP] and sans.rect.y > 5:
        sans.rect.y -= movespeed
    if keys[K_DOWN] and sans.rect.y + sans.rect.height < screenHeight:
        sans.rect.y += movespeed
    if keys[K_ESCAPE]:
        pygame.quit()
        quit()
    if keys[K_SPACE]:
    
        global x
        if x > 20:
            bullet = Bullet()
            bullet.rect.x = sans.rect.x + 40
            bullet.rect.y = sans.rect.y - 20
            bullets.add(bullet)
            allsprites.add(bullet)          
            
            pygame.mixer.Channel(1).set_volume(0.5)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound("audio/blaster.ogg"))
            x = 0
        else:
            x += 10
    else:
        pass
    
a = 0    
m = 0 
xflip = 20
yflip = 20
def move_trump():
    global trump
    global xflip
    global yflip
    global m
    global a
    x = trump.rect.x
    y = trump.rect.y

    tlimit = screenHeight/3
    
    if y >= tlimit or y <= 0:
        yflip = -1 * yflip
    if x + trump.rect.width >= screenWidth or x <= 0:
        xflip = -1 * xflip

    if m == 20:
        a = random.randint(1,400)
        m = 0
    else:
        m = m +1
        pass
            
    if a < 200:
        trump.rect.x += xflip
        #trump.rect.y -= yflip
        #Trump hits something and It doesn't bounce properly. Debug later.

    if  a>= 200:
        trump.rect.y += yflip
        
def load_sounds():
    pygame.mixer.music.load("audio/undertale.mp3")
    pygame.mixer.music.load("audio/blaster.ogg")
    pygame.mixer.music.load("audio/drugs.mp3")
    pygame.mixer.music.load("audio/fired.mp3")
    pygame.mixer.music.load("audio/nein.mp3")
    pygame.mixer.music.load("audio/sue.mp3")
    pygame.mixer.music.load("audio/bye.mp3")
    pygame.mixer.music.load("audio/bingsong.mp3")

def trump_yell():
    yell = random.randint(1, 30)
    if yell == 3:
        pygame.mixer.Channel(3).play(pygame.mixer.Sound("audio/drugs.mp3"))
    if yell == 6:
        pygame.mixer.Channel(4).play(pygame.mixer.Sound("audio/fired.mp3"))
    if yell == 9:
        pygame.mixer.Channel(5).play(pygame.mixer.Sound("audio/nein.mp3"))
    if yell == 12:
        pygame.mixer.Channel(6).play(pygame.mixer.Sound("audio/sue.mp3"))
    if yell == 15:
        pygame.mixer.Channel(7).play(pygame.mixer.Sound("audio/bye.mp3"))
             
pygame.mixer.set_num_channels(10)


def main():
    global sans
    global bullets
    global score
    win = False 
    load_sounds()
    score = 0
    bg = pygame.image.load("images/l1back.jpg").convert_alpha()

    main = True
    pygame.mixer.Channel(0).set_volume(0.8)
    pygame.mixer.Channel(0).play(pygame.mixer.Sound("audio/undertale.mp3"))
    z = 0
    r = 0
    n = 0
    halfh = screenHeight/2
    while main:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                main = False
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]:
            pygame.quit()
            quit()
        
        if win == False:
            move_trump()
            check_keys()
            collidelist = pygame.sprite.spritecollide(trump, bullets, True)
            for bullet in collidelist:
                allsprites.remove(bullet)
                trump_yell()
                score = score + 1
            
        for bullet in bullets:
            if bullet.rect.y > 0:
                bullet.rect.y -= 30
            if bullet.rect.y <= 1:
                bullets.remove(bullet)
                allsprites.remove(bullet)
                    
        screen.fill(black)
 
        font = pygame.font.Font(None, 50)
        text = font.render("Score: %d (270 to Win)" % score, True, white)
    
        screen.blit(bg, [0, 0])
        allsprites.draw(screen)
        screen.blit(text, [10, 0])
        
        if score >= 270:
            winfont = pygame.font.Font(None, 100)
            wintext = winfont.render("YOU HAVE BEAT THE ORANGE MAN, YOU WIN!", True, white)    
            screen.blit(wintext, [30,  halfh])
            win = True
            if r == 0:
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("audio/bingsong.mp3"))
                trump.image = pygame.image.load("images/tlose.png").convert_alpha()
                allsprites.remove(bullets)
                r = 1    
            trump.rect.y -= 10
            if trump.rect.y <= -400:
                allsprites.remove(trump)
    
#        ALWAYS AT THE END
        pygame.display.update()
        clock.tick(24)
                   
main()