import pygame, sys, numpy as np
from pygame.locals import *
# starts game
pygame.init()

# starts myDisplay
#myDisplay = pygame.display.set_mode((1360,768),pygame.FULLSCREEN)
myDisplay = pygame.display.set_mode((800,600))

# sets title
pygame.display.set_caption('This is game!')

# loads marbles
n = 10
seed = pygame.image.load('marble.png').convert()
marbles = [pygame.transform.scale(seed,[20,20]) for i in range(n)]


positions = np.random.random((n,2))*[800,600]
speeds = np.zeros((n,2))

clock = pygame.time.Clock()
t = 0
# main loop

while True:
    clock.tick(30)
    myDisplay.fill((255,255,255))
    for event in pygame.event.get():
        # no key is pressed
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    #evolve
    mice = pygame.mouse.get_pos()
    for i in range(n):
        positions[i] += speeds[i]
        if not(0 < positions[i,0] < 800 and 0 < positions[i,1] < 600):
            speeds[i]*= -1
        else:
            r = positions - positions[i]
            norm = (np.sum(r*r,axis=1))
            norm[i] = 100
            if len(np.argwhere(norm < 20)) > 0:
                pass
            else:
                r_mice = np.array([mice[0],mice[1]])-positions[i]
                a_x = (np.sum(r[:,0]/norm) - 10*r_mice[0]/np.sum(r_mice**2))
                a_y = (np.sum(r[:,1]/norm) - 10*r_mice[1]/np.sum(r_mice**2))
                speeds[i,0] += a_x
                speeds[i,1] += a_y
        marble = marbles[i]
        rect = marble.get_rect()
        rect.center = positions[i]
        myDisplay.blit(marble,rect)
    pygame.display.update()
    pygame.display.flip()
    t += 1
