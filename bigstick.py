import pygame
from ctypes import windll
from yaml import load as yamlLoad
from substick import SubStick
from stick import Stick
from cStringIO import StringIO
from tkFileDialog import askopenfilename

WHITE = (255,255,255)

class BigStick(Stick):
    def __init__(self,stickfaceFileLoc,pos=(0,0)):
        Stick.__init__(self,stickfaceFileLoc,'big.ini',pos)
        self.subSticks = []
        self.keysOut = self.stickfaceIni['keysOut']
        self.keysPressed = []
        self.disableStart = False
        self.startButton = self.stickfaceIni['startButton']
        self.cutoff = 1
        self.text = pygame.font.SysFont('Consolas',20)

    def update(self):
        self.buttons = [0]*12
        self.hat = (0,0)
        for stick in self.subSticks:
            self.buttons = [x+y for x,y in zip(self.buttons,stick.buttons)]
            self.hat = tuple(x+y for x,y in zip(self.hat,stick.hat))

    def draw(self,surface):
        finalImg = self.drawController()
        for b in range(12):
            if self.buttons[b] >= 1:
                textSurf = self.text.render(str(self.buttons[b]), True, WHITE)
                textRect = textSurf.get_rect()
                buttonRect = pygame.Rect(self.buttonLoc[b], self.buttonSize[b])
                textRect.center = buttonRect.center
                finalImg.blit(textSurf,textRect)
        surface.blit(finalImg,self.pos)

    def getNewStickface(self):
        newstickfaceFileLoc = askopenfilename()
        if newstickfaceFileLoc != '':
            self.stickfaceFileLoc = newstickfaceFileLoc
            self.loadStickfaceFile(self.stickfaceFileLoc)
            for stick in self.subSticks:
                stick.loadStickfaceFile(self.stickfaceFileLoc)

    def addSubStick(self,joystick,pos=(0,0)):
        subStick = SubStick(self.stickfaceFileLoc,joystick,pos)
        self.subSticks.append(subStick)

    def changeCutoff(self,i):
        self.cutoff += i
        if self.cutoff > len(self.subSticks):
            self.cutoff = len(self.subSticks)
        if self.cutoff < 1:
            self.cutoff = 1

    def pressKeyDown(self,key):
        vk = windll.user32.VkKeyScanA(ord(key))
        scan = windll.user32.MapVirtualKeyA(vk,0)
        windll.user32.keybd_event(vk,scan,0,0)

    def pressKeyUp(self,key):
        vk = windll.user32.VkKeyScanA(ord(key))
        scan = windll.user32.MapVirtualKeyA(vk,0)
        windll.user32.keybd_event(vk,scan,2,0)

    def sendKeyPresses(self):
        self.keysLastPressed = self.keysPressed
        self.keysPressed = []
        for b in range(8):
            if self.buttons[b] >= self.cutoff:
                self.keysPressed.append(self.keysOut[b])
        start = self.keysOut[self.startButton]
        if self.disableStart and start in self.keysPressed:
            self.keysPressed.remove(start)
        if self.hat[0] < 0:
            self.keysPressed.append(self.keysOut[8]) #left
        if self.hat[0] > 0:
            self.keysPressed.append(self.keysOut[9]) #right
        if self.hat[1] > 0:
            self.keysPressed.append(self.keysOut[10])#up
        if self.hat[1] < 0:
            self.keysPressed.append(self.keysOut[11]) #down

        for key in self.keysPressed:
            if key in self.keysLastPressed:
                self.keysLastPressed.remove(key)
            else:
                self.pressKeyDown(key)
        for key in self.keysLastPressed:
            self.pressKeyUp(key)
