import pygame
from pygbutton import PygButton
from stick import Stick,BigStick
from stickface import *

BLACK = (0,0,0)
WHITE = (255,255,255)
COLUMNS = 2
MAXSTICKS = 8
MAXFPS = 60

pygame.init()

outStick = BigStick(SNESBigStickFace(),(30,30))
numLoadedSticks = min([pygame.joystick.get_count(),MAXSTICKS])
for i in range(numLoadedSticks):
    x = 20 + i%COLUMNS * 140
    y = 220 + i/COLUMNS * 100
    outStick.addSubStick(Stick(SNESStickFace(),i,(x,y)))

ROWS = (len(outStick.subSticks)-1)/2

screen = pygame.display.set_mode((20 + COLUMNS*140, 385 + 100*ROWS))
pygame.display.set_caption('Couch Plays')

fpsClock = pygame.time.Clock()

consolas = pygame.font.SysFont('Consolas',12)

downButton = PygButton((160,340 + 100*ROWS,20,20),'-',)
upButton = PygButton((160,315 + 100*ROWS,20,20),'+')
toggleStartButton = PygButton((20,315 + 100*ROWS,120,20),'Start ENABLED')


done = False
while not(done):

    startTime = int(pygame.time.get_ticks())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if 'click' in upButton.handleEvent(event):
            outStick.changeCutoff(1)
        if 'click' in downButton.handleEvent(event):
            outStick.changeCutoff(-1)
        if 'click' in toggleStartButton.handleEvent(event):
            outStick.disableStart = not(outStick.disableStart)
            if outStick.disableStart:
                toggleStartButton.caption = "Start DISABLED"
            else:
                toggleStartButton.caption = "Start ENABLED"


    screen.fill(BLACK)
    upButton.draw(screen)
    toggleStartButton.draw(screen)
    downButton.draw(screen)
    for stick in outStick.subSticks:
        stick.update()
        stick.draw(screen)
    outStick.update()
    outStick.draw(screen)

    outStick.sendKeyPresses()

    screen.blit(consolas.render("Threshold: %d" % outStick.cutoff, \
        True, WHITE),(185, 330 + 100*ROWS))

    frameTime = int(pygame.time.get_ticks()) - startTime
    screen.blit(consolas.render("Frame time (ms): %d" % frameTime, \
        True, WHITE),(20, 340 + 100*ROWS))

    fps = 1000/frameTime
    if fps > 60:
        fps = 60
    screen.blit(consolas.render("FPS: %d" % fps, True, WHITE), \
        (20, 355 + 100*ROWS))

    fpsClock.tick(MAXFPS)
    pygame.display.update()
