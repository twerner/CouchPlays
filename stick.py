import pygame
from cStringIO import StringIO
from yaml import load as yamlLoad
from zipfile import ZipFile


class Stick(object):

    def __init__(self,stickfaceFileLoc,iniName,pos=(0,0)):
        self.iniName = iniName
        self.stickfaceFileLoc = stickfaceFileLoc
        self.loadStickfaceFile(self.stickfaceFileLoc)
        self.buttons = [0] * len(self.stickfaceIni['buttons'])
        self.hat = (0,0)
        self.pos = pos
        self.cutoff = 1

    def loadStickfaceFile(self,stickfaceFileLoc):
        load = pygame.image.load
        self.stickfaceZip = ZipFile(stickfaceFileLoc,'r')
        self.stickfaceIni = yamlLoad(self.stickfaceZip.read(self.iniName))
        self.controllerSize = tuple(self.stickfaceIni['controllerSize'])
        self.buttonImages = [load(StringIO(self.stickfaceZip.read(i))) for i in self.stickfaceIni['buttonImages']]
        self.controllerImg = load(StringIO(self.stickfaceZip.read(self.stickfaceIni['controllerImage'])))
        self.buttonLoc = [tuple(i) for i in self.stickfaceIni['buttonLocs']]
        self.buttonSize = [tuple(i) for i in self.stickfaceIni['buttonSizes']]

    def drawController(self):
        finalImg = pygame.Surface(self.controllerSize).convert_alpha()
        finalImg.blit(self.controllerImg,(0,0))
        for b in range(12):
            if self.buttons[b] >= self.cutoff:
                finalImg.blit(self.buttonImages[b],self.buttonLoc[b])
        return finalImg


