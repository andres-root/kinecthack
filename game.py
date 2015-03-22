import pygame, sys, numpy as np
from pygame.locals import *
# starts game
pygame.init()

# starts myDisplay
#myDisplay = pygame.display.set_mode((1360,768),pygame.FULLSCREEN)
len_x,len_y = 800,600
myDisplay = pygame.display.set_mode((len_x,len_y))

background = pygame.image.load('background.jpg')

# sets title
pygame.display.set_caption('This is game!')

# loads marbles
n = 2
seed = pygame.image.load('planet.png')
seed = pygame.transform.scale(seed,[20,20])
seed = seed.convert_alpha()
marbles = [seed for i in range(n)]


positions = np.random.random((n,2))*[len_x,len_y]
speeds = np.zeros((n,2))

clock = pygame.time.Clock()
t = 0
# main loop

while True:
    clock.tick(30)
    myDisplay.fill((255,255,255))
    myDisplay.blit(background, [0,0])
    mice = np.array(pygame.mouse.get_pos())
    for event in pygame.event.get():
        # no key is pressed
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            n += 1
            marbles.append(seed)
            positions = np.reshape(np.append(positions,mice),(n,2))
            speeds = np.reshape(np.append(speeds,np.zeros(2)),(n,2))
        if event.type == KEYDOWN:
            if event.key == K_c:
                n += 1
                marbles.append(seed)
                positions = np.reshape(np.append(positions,mice),(n,2))
                speeds = np.reshape(np.append(speeds,np.zeros(2)),(n,2))
    #evolve
    for i in range(n):
        positions[i] += speeds[i]
        if not(0 < positions[i,0] < len_x and 0 < positions[i,1] < len_y):
            speeds[i]*= -1
        else:
            r = positions - positions[i]
            norm = (np.sum(r*r,axis=1))
            norm[i] = 100
            if len(np.argwhere(norm < 20)) > 0:
                pass
            else:
                r_mice = mice-positions[i]
                d_mice = np.sum(r_mice**2)
                a_x = 5*(np.sum(r[:,0]/norm))
                a_y = 5*(np.sum(r[:,1]/norm))
                if d_mice > 40:
                    a_x -= 10*r_mice[0]/d_mice
                    a_y -= 10*r_mice[1]/d_mice
                speeds[i,0] += a_x
                speeds[i,1] += a_y
        marble = marbles[i]
        rect = marble.get_rect()
        rect.center = positions[i]
        myDisplay.blit(marble,rect)
    pygame.display.update()
    pygame.display.flip()
    t += 1
