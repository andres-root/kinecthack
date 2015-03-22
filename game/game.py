import pygame, sys, numpy as np
import cv2
from pygame.locals import *
# doesnt starts game
#pygame.init()


################################################################################
#aqui empieza :)
cap = cv2.VideoCapture(0)


# take first frame of the video
ret, frame = cap.read()

# setup initial location of window
r, h, c, w = 250, 90, 400, 125  # simply hardcoded the values
track_window = (c, r, w, h)

# set up the ROI for tracking
roi = frame[r:r+h,  c:c+w]
hsv_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv_roi,  np.array((0.,  60., 32.)),  np.array((180., 255., 255.)))
roi_hist = cv2.calcHist([hsv_roi], [0], mask, [180], [0, 180])
cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)

# Setup the termination criteria,  either 10 iteration or move by atleast 1 pt
term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,  10,  1)
################################################################################

# starts myDisplay
#myDisplay = pygame.display.set_mode((1360,768),pygame.FULLSCREEN)
len_x,len_y = 800,600
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
hand = pygame.image.load('planets/hand.png')
hand = pygame.transform.scale(hand,[100,100])
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
run = False
# main loop

while True:

################################################################################
#again
    ret, frame = cap.read()

    if ret is True:
        hsv = cv2.cvtColor(frame,  cv2.COLOR_BGR2HSV)
        dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)

        # apply meanshift to get the new location
        ret,  track_window = cv2.meanShift(dst,  track_window,  term_crit)

        # Draw it on image
        x,  y,  w,  h = track_window
        cv2.rectangle(frame,  (x,  y),  (x+w,  y+h),  255,  2)
        cv2.imshow('img2',  frame)
        posHand = [x+w*0.5,y+h*0.5]
################################################################################
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

            if event.key == K_p:
                run = not run

        if event.type == pygame.MOUSEBUTTONUP:
            n += 1
            R = positions[0] - mice
            v = np.sqrt(G*m_sun)*np.array([R[1],-R[0]])/np.sqrt(np.sum(R*R))
            marbles.append(seed(np.random.randint(0,10)))
            positions = np.reshape(np.append(positions,mice),(n,2))
            speeds = np.reshape(np.append(speeds,v),(n,2))
            mass = np.append(mass,m_pla)

    #evolve

    for j in range(n):
        i = n-j-1
        if run:
            positions[i] += speeds[i]
            if not(0 < positions[i,0] < len_x and 0 < positions[i,1] < len_y):
                speeds[i]*= -1
                #positions[i,0]%=len_x
                #positions[i,1]%=len_y

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

                    speeds[i,0] += a_x
                    speeds[i,1] += a_y
        marble = marbles[i]
        rect = marble.get_rect()
        rect.center = positions[i]
        myDisplay.blit(marble,rect)

    recthand = hand.get_rect()
    recthand.center = posHand
    myDisplay.blit(hand,recthand)
    pygame.display.update()
    pygame.display.flip()
    t += 1

cv2.destroyAllWindows()
cap.release()
