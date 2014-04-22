import pygame
from ctypes import windll
from stickface import *

pygame.init()

bigText = pygame.font.SysFont('Consolas',20)
WHITE = (255,255,255)

class Stick(object):

    def __init__(self,stickface,i=-1,pos=(0,0)):
        if i != -1:
            self.stick = pygame.joystick.Joystick(i)
            self.stick.init()
        self.pos = pos
        self.size = stickface.size
        self.buttonImages = stickface.buttonImages
        self.controllerImg = stickface.controller
        self.buttonLoc = stickface.buttonLoc
        self.buttonSize = stickface.buttonSize
        self.buttons = [0]*12
        self.hat = (0,0)
        self.cutoff = 1

    def update(self):
        self.buttons = [self.stick.get_button(b) for b in range(8)]
        self.buttons = self.buttons + [0]*4 #add dpad
        self.hat = self.stick.get_hat(0)
        hatX,hatY = self.hat
        if hatX == -1: self.buttons[8] += 1 #left
        if hatX == 1: self.buttons[9] += 1 #right
        if hatY == 1: self.buttons[10] += 1 #up
        if hatY == -1: self.buttons[11] += 1 #down

    def makeSurface(self):
        finalImg = pygame.Surface(self.size).convert_alpha()
        finalImg.blit(self.controllerImg,(0,0))
        for b in range(12):
            if self.buttons[b] >= self.cutoff:
                loc = self.buttonLoc[b]
                finalImg.blit(self.buttonImages[b],loc)
        return finalImg

    def draw(self,surface):
        finalImg = self.makeSurface()
        surface.blit(finalImg,self.pos)

class BigStick(Stick):
    def __init__(self,stickface,pos=(0,0)):
        Stick.__init__(self,stickface,-1,pos)
        self.dpadButtons = [0,0,0,0]
        self.subSticks = []
        self.keysOut = stickface.keysOut
        self.keysPressed = []
        self.disableStart = False
        self.startButton = stickface.startButton

    def update(self):
        self.buttons = [0]*12
        self.hat = (0,0)
        for stick in self.subSticks:
            self.buttons = [x+y for x,y in zip(self.buttons,stick.buttons)]
            self.hat = tuple(x+y for x,y in zip(self.hat,stick.hat))

    def draw(self,surface):
        finalImg = self.makeSurface()
        for b in range(12):
            if self.buttons[b] >= 1:
                textSurf = bigText.render(str(self.buttons[b]), True, WHITE)
                textRect = textSurf.get_rect()
                buttonRect = pygame.Rect(self.buttonLoc[b], self.buttonSize[b])
                textRect.center = buttonRect.center
                finalImg.blit(textSurf,textRect)
        surface.blit(finalImg,self.pos)

    def addSubStick(self,stick):
        self.subSticks.append(stick)

    def changeCutoff(self,i):
        self.cutoff += i
        if self.cutoff > len(self.subSticks):
            self.cutoff = len(self.subSticks)
        if self.cutoff < 1:
            self.cutoff = 1

    def keyDown(self,key):
        vk = windll.user32.VkKeyScanA(ord(key))
        scan = windll.user32.MapVirtualKeyA(vk,0)
        windll.user32.keybd_event(vk,scan,0,0)


    def keyUp(self,key):
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
                self.keyDown(key)
        for key in self.keysLastPressed:
            self.keyUp(key)

