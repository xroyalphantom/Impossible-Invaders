import sys, random, time, math, random
import pygame
from bullet import Bullet
from spaceship import Spaceship
from ssbullet import SSBullet

pygame.init()

size = width, height = 1280, 800
speed = [0, 0]
bulletEntities = []
ssBulletEntities = []
ssList = [] 
shieldrectlist = []
color = 0, 0, 0
tick = 0
interval = 40
movingRight = True
movingDown = False
heldDown = False
cooldown = 0
lives = 3

ss_spawn_x = []

for i in range(1,11):
    for j in range(1,5):
        ss_spawn_x.append((80*i,80*j))

for i in range(0,5):
    bulletEntities.append(Bullet(i))

for i in range(0,10):
    ssBulletEntities.append(SSBullet(i))

for i in range(0,4):
    shieldrectlist.append(pygame.Rect(i*width/4+120,height*3/4,40,40))
    shieldrectlist.append(pygame.Rect(i*width/4+160,height*3/4,40,40))
    shieldrectlist.append(pygame.Rect(i*width/4+120,height*3/4-40,40,40))
    shieldrectlist.append(pygame.Rect(i*width/4+160,height*3/4-40,40,40))

screen = pygame.display.set_mode(size)

ball = pygame.image.load("tank.png")
ballrect = ball.get_rect()
ballrect.center = (width/2,height - 80)

heart = pygame.image.load("heart.png")
background = pygame.image.load("background.png")
background = pygame.transform.scale(background,size)

shieldfragment = pygame.image.load("shieldfragment.png")
shieldfragment = pygame.transform.scale(shieldfragment,(40,40))

youwin = pygame.image.load("youwin.png")
youwin = pygame.transform.scale(youwin,(640,400))
youwinrect = youwin.get_rect()
youwinrect.center = (width/2,height/2)

gameover = pygame.image.load("gameover.png")
gameover = pygame.transform.scale(gameover,(640,400))
gameoverrect = gameover.get_rect()
gameoverrect.center = (width/2,height/2)

# Spawn the ships
for i in range(0,40):
    SS = Spaceship(i)
    SS.set_coordinates(ss_spawn_x[i])
    ssList.append(SS)

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.key == pygame.K_LEFT:
                heldDown = True
                speed[0] = -5
            if event.key == pygame.K_RIGHT:
                heldDown = True
                speed[0] = 5
            #if event.key == pygame.K_UP:
                #heldDown = True
                #speed[1] = -5
            #if event.key == pygame.K_DOWN:
                #heldDown = True
                #speed[1] = 5
            if event.key == pygame.K_SPACE:
                if cooldown == 0:
                    cooldown = 50
                    for i in bulletEntities:
                        if i.available == True:
                            i.set_coordinates(ballrect.midtop)
                            i.set_avail(False)
                            break
                        else:
                            continue
                

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                heldDown = False
                speed[0] = 0
            elif event.key == pygame.K_RIGHT:
                heldDown = False
                speed[0] = 0
            #elif event.key == pygame.K_UP:
                #heldDown = False
                #speed[1] = 0
            #elif event.key == pygame.K_DOWN:
                #heldDown = False
                #speed[1] = 0

    if heldDown:
        if ballrect.midleft[0]+speed[0] > 0 and ballrect.midright[0]+speed[0] < width:
            ballrect = ballrect.move(speed)

    screen.fill(color)
    screen.blit(background, (0,0))

    # Random bullet interval
    bulletInterval = interval + random.randint(10,20)

    # Random SS firing
    if tick % bulletInterval == 0:
        randomSS = ssList[random.randint(0,len(ssList)-1)]
        for i in ssBulletEntities:
            if i.available:
                i.set_coordinates(randomSS.rect.midtop)
                i.set_avail(False)
                break
            else:
                continue

    for i in bulletEntities:
        if i.available == False:
            i.rect = i.rect.move(i.speed)
            screen.blit(i.image, i.rect)

            if not pygame.Rect(0, 0, width, height).collidepoint(i.rect.midbottom[0],i.rect.midbottom[1]):
                i.set_avail(True)
            for j in ssList:
                if i.rect.colliderect(j.rect):
                    ssList.remove(j)
                    i.set_avail(True)
                    break
            
            for j in shieldrectlist:
                if i.rect.colliderect(j):
                    shieldrectlist.remove(j)
                    i.set_avail(True)
                    break

    for i in ssBulletEntities:
        if i.available == False:
            i.rect = i.rect.move(i.speed)
            screen.blit(i.image, i.rect)

            if not pygame.Rect(0, 0, width, height).collidepoint(i.rect.midbottom[0],i.rect.midbottom[1]):
                i.set_avail(True)
            if i.rect.colliderect(ballrect):
                i.set_avail(True)
                lives -= 1
            
            for j in shieldrectlist:
                if i.rect.colliderect(j):
                    shieldrectlist.remove(j)
                    i.set_avail(True)
                    break

    screen.blit(ball, ballrect)

    for i in range(1,lives+1):
        screen.blit(heart, (i*50-30, 10))

    # Check if any spaceship has hit the screen edges
    if tick % interval == 0:
        for i in ssList:
            if i.rect.bottom > height-80:
                screen.fill(color)
                screen.blit(gameover,gameoverrect)
                pygame.display.flip()
                time.sleep(4)
                pygame.quit()
                sys.exit()
            # Check for right-most or left-most
            if movingRight:
                if i.rect.right > width-20:
                    movingRight = False
                    movingDown = True
                    break
            else:
                if i.rect.left < 20:
                    movingRight = True
                    movingDown = True
                    break

    # Movement of ss / interval
    for i in ssList:
        if tick % interval == 0:
            if movingDown:
                i.rect.move_ip(0,30)
            elif movingRight:
                i.rect.move_ip(20,0)
            else:
                i.rect.move_ip(-20,0)
        screen.blit(i.image, i.rect) 

    movingDown = False
    
    interval = len(ssList)

    for i in shieldrectlist:
        screen.blit(shieldfragment,i)

    if len(ssList) == 0:
        screen.fill(color)
        screen.blit(youwin,youwinrect)
        pygame.display.flip()
        time.sleep(4)
        pygame.quit()
        sys.exit()

    if lives == 0:
        screen.fill(color)
        screen.blit(gameover,gameoverrect)
        pygame.display.flip()
        time.sleep(4)
        pygame.quit()
        sys.exit()

    # Display/tick update
    pygame.display.flip()
    tick += 1
    if cooldown > 0:
        cooldown -= 1