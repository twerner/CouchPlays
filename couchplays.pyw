import pygame
from pygbutton import PygButton
from bigstick import BigStick
try:  # Python 2.x support
    from Tkinter import Tk
except ImportError:  # Python 3.X support
    from tkinter import Tk

BLACK = (0,0,0)
WHITE = (255,255,255)
COLUMNS = 2
MAXSTICKS = 8
MAXFPS = 60

pygame.init()

outStick = BigStick('SNES.zip',(30,30))
numLoadedSticks = min([pygame.joystick.get_count(),MAXSTICKS])
for i in range(numLoadedSticks):
    x = 20 + i%COLUMNS * 140
    y = 220 + i/COLUMNS * 100
    tempJoystick = pygame.joystick.Joystick(i)
    outStick.addSubStick(tempJoystick,(x,y))

ROWS = int((len(outStick.subSticks)-1)/2)

Tk().withdraw() #suppress Tkinter window
screen = pygame.display.set_mode((20 + COLUMNS*140, 25 + 385 + 100*ROWS))
pygame.display.set_caption('Couch Plays')

fpsClock = pygame.time.Clock()

consolas = pygame.font.SysFont('Consolas',12)

downButton = PygButton((160,340 + 100*ROWS,20,20),'-',)
upButton = PygButton((160,315 + 100*ROWS,20,20),'+')
toggleStartButton = PygButton((20,315 + 100*ROWS,120,20),'Start ENABLED')
stickfaceButton = PygButton((20,370 + 100*ROWS,120,20),'New stickface')


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
        if 'click' in stickfaceButton.handleEvent(event):
            outStick.getNewStickface()


    screen.fill(BLACK)
    upButton.draw(screen)
    toggleStartButton.draw(screen)
    downButton.draw(screen)
    stickfaceButton.draw(screen)
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
