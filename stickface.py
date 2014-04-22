import pygame

class SNESStickFace(object):
    load = pygame.image.load
    controller = load('images/controller-half.png')
    button = load('images/button-half.png')
    shoulder = load('images/shoulder-half.png')
    start = load('images/startselect-half.png')
    left = load('images/Dleft-half.png')
    right = load('images/Dright-half.png')
    up = load('images/Dup-half.png')
    down = load('images/Ddown-half.png')
    buttonImages = [button]*4 + [shoulder]*2 + [start]*2 + \
        [left,right,up,down]
    size = (120,80)
    buttonLoc = [
        (81,58), (98,41), (64,41), (81,24),
        (2,2),   (78,2),  (45,20), (63,20),
        (3,45),  (34,45), (19,29), (19,60)]
    buttonSize = [
        (20,20), (20,20), (20,20), (20,20),
        (40,18), (40,18), (12,12), (12,12),
        (17,16), (17,16), (16,17), (16,17)]


class SNESBigStickFace(object):
    load = pygame.image.load
    controller = load('images/controller-full.png')
    button = load('images/button-full.png')
    shoulder = load('images/shoulder-full.png')
    start = load('images/startselect-full.png')
    up = load('images/Dup-full.png')
    down = load('images/Ddown-full.png')
    left = load('images/Dleft-full.png')
    right = load('images/Dright-full.png')
    buttonImages = [button]*4 + [shoulder]*2 + [start]*2 + \
        [left,right,up,down]

    size = (240,160)
    buttonLoc = [
        (162,116), (196,82), (128,82), (162,48),
        (4,4),     (156,4),  (90,40),  (126,40),
        (6,90),    (67,90),  (38,58),  (38,119)]
    buttonSize = [
        (40,40), (40,40), (40,40), (40,40),
        (80,36), (80,36), (24,24), (24,24),
        (36,32), (36,32), (32,36), (32,36)]
    dpadLoc = (6,58)
    dpadSize = (96,96)
    #Xbox - [A, B, X, Y, LB, RB, Back, Start, left, right, up, down]
    #PS3 - [X, O, [], ^, L1, R1, Select, Start, left, right, up, down]
    #SNES - [B, A, Y, X, L, R, Select, Start, left, right, up, down]
    keysOut = ['j','k','l','u','n','m','g','h','a','d','w','s']
    startButton = 7
