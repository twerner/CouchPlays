import pygame
from stick import Stick
from stickwrapper import StickWrapper

consolas = pygame.font.SysFont('Consolas',12)
RED = (255,0,0)


class SubStick(Stick):

    def __init__(self,stickfaceFileLoc,joystick=None,pos=(0,0)):
        Stick.__init__(self,stickfaceFileLoc,'small.ini',pos)
        if joystick != None:
            self.stick = StickWrapper(joystick)
            self.stickName = self.stick.realStick.get_name()
            self.stickID = self.stick.realStick.get_id()

    def update(self):
        self.buttons = self.stick.getAllButtons()
        self.buttons = self.buttons + [0]*4 #add dpad
        self.hat = self.stick.getHat()
        hatX,hatY = self.hat
        if hatX == -1: self.buttons[8] += 1 #left
        if hatX == 1: self.buttons[9] += 1 #right
        if hatY == 1: self.buttons[10] += 1 #up
        if hatY == -1: self.buttons[11] += 1 #down

    def draw(self,surface):
        finalImg = self.drawController()
        finalImg.blit(consolas.render(str(self.stickID), True, RED), (0,0))
        surface.blit(finalImg,self.pos)

