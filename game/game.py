import pygame, sys, numpy as np
from pygame.locals import *
# starts game
pygame.init()

# starts myDisplay
#myDisplay = pygame.display.set_mode((1360,768),pygame.FULLSCREEN)
len_x,len_y = 1366,768
myDisplay = pygame.display.set_mode((len_x,len_y))

background = pygame.image.load('background.jpg')

# sets title
pygame.display.set_caption('God in a box')

# loads marbles
n = 1

names = ['planets/'+str(i)+'.png' for i in range(10)]
def seed(n):
    ans = pygame.image.load(names[n])
    ans = pygame.transform.scale(ans,[20,20])
    return ans

sun = pygame.image.load('planets/sun1.png')
sun = pygame.transform.scale(sun,[80,80])
m_pla = 1
m_sun = 500*m_pla
G = 0.1
marbles = [sun]


positions = np.zeros((n,2))
speeds = np.zeros((n,2))
mass = np.empty(n)

positions[0] =np.array([len_x,len_y])/2
mass[0] = m_sun
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

        if event.type == KEYUP:
            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            n += 1
            R = positions[0] - mice
            v = -np.sqrt(G*m_sun)*np.array([R[1],-R[0]])/np.sqrt(np.sum(R*R))
            marbles.append(seed(np.random.randint(0,10)))
            positions = np.reshape(np.append(positions,mice),(n,2))
            speeds = np.reshape(np.append(speeds,v),(n,2))
            mass = np.append(mass,m_pla)

    #evolve
    for i in range(n):
        positions[i] += speeds[i]
        if not(0 < positions[i,0] < len_x and 0 < positions[i,1] < len_y):
            speeds[i]*= -1
        else:
            r = positions - positions[i]
            norm = (np.sum(r*r,axis=1))
            norm[i] = 100
            boing = np.argwhere(norm < 80)
            if len(boing) > 0:
                speeds[i,0],speeds[i,1] = speeds[i,1],-speeds[i,0]
                #speeds[boing,0],speeds[boing,1] = -speeds[boing,1],speeds[boing,0] 
                pass
            else:
                r_mice = mice-positions[i]
                d_mice = np.sum(r_mice**2)
                a_x = G*(np.sum(mass*r[:,0]/norm))
                a_y = G*(np.sum(mass*r[:,1]/norm))
                if d_mice > 40:
                    a_x -= 0*G*r_mice[0]/d_mice
                    a_y -= 0*G*r_mice[1]/d_mice
                speeds[i,0] += a_x
                speeds[i,1] += a_y
        marble = marbles[i]
        rect = marble.get_rect()
        rect.center = positions[i]
        myDisplay.blit(marble,rect)
    pygame.display.update()
    pygame.display.flip()
    t += 1
