'''
Created on Dec 4, 2022

@author: Brandon Demeritt
'''

#IMPORTS
import pygame, sys
from pygame.locals import *
import random, time

 
pygame.init()

#Handle FPS and Clock 
FPS = 60
FramePerSec = pygame.time.Clock()
 
#Predefined some colors
RED   = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

 
#Screen information
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 720
score = 0

#Starting X Coordinates
playerXCoord = 325

#Window, title, icon setup
font = pygame.font.SysFont("Lucida Calligraphy", 60)
fontSmall = pygame.font.SysFont("Lucida Calligraphy", 20)
gameOver = font.render("Game Over", True, RED)

 
DISPLAYSURF = pygame.display.set_mode((700,720))
DISPLAYSURF.fill(BLACK)
pygame.display.set_caption("Space Game")
pygame.display.set_icon(pygame.image.load("z.png"))
 
#Enemy Class object, random start location at the top of screen.  Move down at a set speed, kill object if gets to bottom.
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40),0) 
 
    def move(self):
        self.rect.move_ip(0,6)
        if (self.rect.bottom > 740):
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)
 
 
#Player Class.  Sets player ship object, methods to move and fire bullets (in the move method). 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.image = pygame.image.load("playerShip.png")
        self.rect = self.image.get_rect()
        self.rect.center = (325, 620)
 
    def move(self):
        held_keys = pygame.key.get_pressed()
        global playerXCoord
        if self.rect.left > 0:
            if held_keys[K_LEFT]:
                self.rect.move_ip(-6, 0)
                playerXCoord -= 6
        if self.rect.right < SCREEN_WIDTH:        
            if held_keys[K_RIGHT]:
                self.rect.move_ip(6, 0)
                playerXCoord += 6
        if held_keys[K_SPACE]:
            bullet = Bullet(playerXCoord)
            bullets.add(bullet)
            allSprites.add(bullet)
            
#Bullet class object.  Creates bullets to travel from the ship and upwards.
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y=620):
        super().__init__()
        self.x = x
        self.y = 620
        global playerXCoord
        self.image = pygame.image.load("bullet.png") 
        self.rect = self.image.get_rect()
        self.rect.center = (playerXCoord, 620)
        
    def move(self):
        self.rect.move_ip(0, -30)
        if self.rect.bottom < 10:
            self.kill()


#Starting assignments
P1 = Player()
E1 = Enemy()
enemies = pygame.sprite.Group()
enemies.add(E1)
bullets = pygame.sprite.Group()
allSprites = pygame.sprite.Group()
allSprites.add(P1)
allSprites.add(E1)

#Game Loop
while True:     
    
    #Check for quit
    for event in pygame.event.get():              
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
            
    #Set screen background and score
    DISPLAYSURF.fill(BLACK)
    scores = fontSmall.render(str(score), True, WHITE)
    DISPLAYSURF.blit(scores, (10,10))
    endScore = "Score: " + str(score)
    endGameScore = font.render(endScore, True, RED)
    
    #Moving objects
    for entity in allSprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
    
    #Checks for enemy collision with bullets, if true, deletes enemy, creates new enemy, and add points to score.
    for enemy in enemies:
        if pygame.sprite.spritecollideany(E1, bullets):
            enemy.kill()
            E1 = Enemy()
            enemies.add(E1)
            allSprites.add(E1)
            score += 10
        
    #Check for player collision with enemy.  If true, end game, play sound effects, show game over screen
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("Bomb.mp3").play()
        time.sleep(3)
        
        #Open and append score to highscore file
        highscores = open("highscores.txt", 'a')
        highscores.write(str(score) + "\n")
        highscores.close()
        #Show Game Over and Score
        DISPLAYSURF.blit(gameOver, (150, 300))
        DISPLAYSURF.blit(endGameScore, (150, 375))
        
        
        '''
        Was unable to fully get the sorting working right, it's sorting as a string, not integers.  Having trouble getting that worked out, but it does save to the file and reads it.
        '''
        #Show Top 3 High scores
        highscoresfile = open("highscores.txt", 'r')
        highscorescontents = highscoresfile.read()
        highscoreslist = highscorescontents.split("\n")
        highscoreslist.sort(reverse = True)
        if len(highscorescontents) > 3:
            highScore1 = str(highscoreslist[0])
            highScore2 = str(highscoreslist[1])
            highScore3 = str(highscoreslist[2])
            top3 = "Top 3 High Scores"
            top3scores = font.render(top3, True, RED)
            endHighScore1 = font.render(highScore1, True, RED)
            endHighScore2 = font.render(highScore2, True, RED)
            endHighScore3 = font.render(highScore3, True, RED)
            DISPLAYSURF.blit(top3scores, (100, 20))
            DISPLAYSURF.blit(endHighScore1, (150, 75))
            DISPLAYSURF.blit(endHighScore2, (150, 150))
            DISPLAYSURF.blit(endHighScore3, (150, 225))
        highscoresfile.close()
        
        
        #Update and freeze screen
        pygame.display.update()
        time.sleep(6)
        
        #quit game
        pygame.quit()
        sys.exit()
    

         
    pygame.display.update()
    FramePerSec.tick(FPS)