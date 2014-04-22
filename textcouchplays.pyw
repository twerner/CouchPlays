import pygame
from pygame.locals import *
from ctypes import windll

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)

# This is a simple class that will help us print to the screen
# It has nothing to do with the joysticks, just outputing the
# information.
class TextPrint:
    def __init__(self,screen):
        self.screen = screen
        self.reset()
        self.font = pygame.font.Font(None, 20)

    def write(self, textString):
        textBitmap = self.font.render(textString, True, BLACK)
        self.screen.blit(textBitmap, [self.x, self.y])
        self.y += self.line_height

    def skipline(self):
        self.y += self.line_height

    def reset(self):
        self.x = 10
        self.y = 10
        self.line_height = 15

    def indent(self):
        self.x += 10

    def unindent(self):
        self.x -= 10

# from the internet
KEYDOWN = 0
KEYUP = 2

def key_down( vk ) :
    scan = windll.user32.MapVirtualKeyA(vk,0)
    windll.user32.keybd_event(vk,scan,KEYDOWN,0)


def key_up( vk ) :
    scan = windll.user32.MapVirtualKeyA(vk,0)
    windll.user32.keybd_event(vk,scan,KEYUP,0)


letterDict = {
    'w':87, #up
    'a':65, #left
    's':83, #down
    'd':68, #right
    'g':71, #select
    'h':72, #start
    'j':74, #button1
    'k':75, #button2
    'l':76, #button3
    'u':85, #button4
    'i':73, #button5
    'o':79, #button6
    'n':78, #left shoulder
    'm':77  #right shoulder
}

keysPressed = []
#[A, B, X, Y, LB, RB, Back, Start, LS, RS]
#[X, O, [], ^, L1, R1, Select, Start, L3, R3]
buttonConvert = ['j','k','u','i','n','m','g','h','o','l']

pygame.init()

# Set the width and height of the screen [width,height]
size = [300, 700]
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Couch Plays - Text Version')

tp = TextPrint(screen)

sticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]

for stick in sticks:
    stick.init()

FPS = 60
fpsClock = pygame.time.Clock()
lol = 0

done = False

while not(done):
    startTime = int(pygame.time.get_ticks())

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True # Flag that we are done so we exit this loop

    screen.fill(WHITE)
    tp.reset()
    tp.write('Number of joysticks: %d' % len(sticks))
    tp.skipline()

    outHat = (0,0)
    outButtons = [0,0,0,0,0,0,0,0,0,0] #10 buttons on Xbox controller
    #[A, B, X, Y, LB, RB, Back, Start, LS, RS]
    #[X, O, [], ^, L1, R1, Select, Start, L3, R3]

    for s in range(len(sticks)):
        stick = sticks[s]
        tp.write("Joystick #%d" % int(s+1))
        tp.indent()

        hat = stick.get_hat(0)
        outHat = tuple(sum(x) for x in zip(outHat,hat))
        tp.write("Hat value: %s" % str(hat))

        buttons = []
        for b in range(stick.get_numbuttons()):
            if stick.get_button(b):
                buttons.append(1)
                outButtons[b] += 1
            else:
                buttons.append(0)
        tp.write("Button values: %s" % str(buttons))

        tp.unindent()
        tp.skipline()

    tp.write("Output joystick")
    tp.indent()
    tp.write("Hat value: %s" % str(outHat))
    tp.write("Button values: %s" % str(outButtons))
    tp.unindent()
    tp.skipline()

    keysLastPressed = keysPressed
    keysPressed = []

    xHat, yHat = outHat
    if xHat > 0:
        keysPressed.append('d')
    elif xHat < 0:
        keysPressed.append('a')
    if yHat > 0:
        keysPressed.append('w')
    elif yHat < 0:
        keysPressed.append('s')

    for b in range(len(outButtons)):
        if outButtons[b]:
            keysPressed.append(buttonConvert[b])

    for key in keysPressed:
        if key in keysLastPressed:
            keysLastPressed.remove(key)
        key_down(letterDict[key])
    for key in keysLastPressed:
        key_up(letterDict[key])

    tp.write("Keys pressed: %s" % keysPressed)
    tp.skipline()

    frameTime = int(pygame.time.get_ticks()) - startTime
    tp.write("Frame time (ms): %d" % frameTime)

    fpsClock.tick(FPS)

    pygame.display.update()

pygame.quit()
