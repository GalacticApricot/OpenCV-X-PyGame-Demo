import cv2, imutils
import time
import numpy as np
import pygame, random
from car import Car
 
tracker = cv2.TrackerCSRT_create()
video  = cv2.VideoCapture(0)
_,frame = video.read()
frame = imutils.resize(frame,width=720)
BB = cv2.selectROI(frame,False)
tracker.init(frame, BB)
 
pygame.init()
 
GREEN = (20, 255, 140)
GREY = (210, 210 ,210)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PURPLE = (255, 0, 255)
BLACK = (0, 0, 0)
        
SCREENWIDTH=720
SCREENHEIGHT=500
 
size = (SCREENWIDTH, SCREENHEIGHT)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("TRACK_X_DISPLAY")
 
all_sprites_list = pygame.sprite.Group()
 
playerCar = Car(RED, 60, 30)
playerCar.rect.x = 200
playerCar.rect.y = 300

apples = []
score = 0
frameno = 0
gametime = 0
font = pygame.font.Font('freesansbold.ttf', 32)
font2 = pygame.font.Font('freesansbold.ttf', 16)
scoretext = None
scoreRect = None
timetext = None
timeRect = None
ended = False

def createapple():
    global apples
    x = random.randint(20, 700)
    appleCar = Car(GREEN, 15, 15)
    appleCar.rect.x = x
    appleCar.rect.y = 0
    apples.append(appleCar)
    all_sprites_list.add(appleCar)

def crashwith(otherobjx, otherobjy, otherobjwidth, otherobjheight):
    myleft = playerCar.rect.x
    myright = playerCar.rect.x + 60
    mytop = playerCar.rect.y
    mybottom = playerCar.rect.y + 30
    otherleft = otherobjx
    otherright = otherobjx + otherobjwidth
    othertop = otherobjy
    otherbottom = otherobjy + otherobjheight
    crash = True
    if mybottom < othertop or mytop > otherbottom or myright < otherleft or myleft > otherright:
        crash = False
    return crash

def updategame():
    global apples, frameno, all_sprites_list, gametime, score, ended, scoretext, scoreRect, createapple, crashwith, timetext, timeRect, font
    frameno += 1
    if frameno & 583 == 0:
        createapple()
    for apple in apples:
        apple.rect.y += 7
        if crashwith(apple.rect.x, apple.rect.y, 15, 15):
            for i, v in enumerate(apples):
                if apple == v:
                    apples.pop(i)
            all_sprites_list.remove(apple)
            apple.kill()
            score += 1
        if apple.rect.y == SCREENHEIGHT:
            for i, v in enumerate(apples):
                if apple == v:
                    apples.pop(i)
            all_sprites_list.remove(apple)
            apple.kill()
    if frameno != 0 and frameno & 60 == 0:
        gametime += 1
    if gametime == 30:
        ended = True
    scorestring = 'Score: ' + str(score)
    scoretext = font.render(scorestring, True, GREEN, WHITE)
    scoreRect = scoretext.get_rect()
    scoreRect.center = (100, 20)
    timestring = 'Time: ' + str(30 - gametime)
    timetext = font.render(timestring, True, RED, WHITE)
    timeRect = timetext.get_rect()
    timeRect.center = (SCREENWIDTH - 100, 20)
 
 
 
all_sprites_list.add(playerCar)
 
 
clock=pygame.time.Clock()
 
 
 
while True:
    _,frame = video.read()
    frame = imutils.resize(frame,width=720)
    img_rgb=frame.copy()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    track_success,BB = tracker.update(frame)
    if track_success:
        if not ended:
            top_left = (int(BB[0]),int(BB[1]))
            bottom_right = (int(BB[0]+BB[2]), int(BB[1]+BB[3]))
            cv2.rectangle(img_rgb,top_left,bottom_right,(0,255,0),5)
            cv2.imshow('Output',img_rgb)
            key  =  cv2.waitKey(1) & 0xff       
            posstr = str(bottom_right)
            
            headpos = posstr.split(', ')
            
            
            headxbr = headpos[0]
            headybr = headpos[1]
            headxstr = headxbr.strip('(')
            headystr = headybr.strip(')')
            headx = int(headxstr)
            heady = int(headystr)
            
            
            
            playerCar.x(headx)
            playerCar.y(heady)
            updategame()
            all_sprites_list.update()
            screen.fill(WHITE)
            screen.blit(scoretext, scoreRect)
            screen.blit(timetext, timeRect)
            all_sprites_list.draw(screen)
        else:
            screen.fill(WHITE)
            crashstring = 'Game Over. Score: ' + str(score)
            crashtext = font2.render(crashstring, True, GREEN, BLACK)
            crashRect = crashtext.get_rect()
            crashRect.center = (SCREENWIDTH / 2, SCREENHEIGHT / 2)
            screen.blit(crashtext, crashRect)
        pygame.display.flip()
        clock.tick(60)
        
    if key == ord('q'):
        break
video.release()
cv2.destroyAllWindows()
