import pygame, sys, random
from pygame.locals import *
from graphical_elements import *
import game_variables as data
import game_engine

                                                                
clock = pygame.time.Clock()
RUNNING = True
scroll_y = 0

txtl = {
    air : 'Air',
    battery : 'Battery',
    brick : 'Brick',
    heat: 'Heater',
    lava :  'Lava',
    sand : 'Sand',
    steam     : 'Steam',
    water : 'Water',
    wire : 'Wire',
    heatingHeat :  'Powered Heater',
    poweredWire : 'Powered Wire',
    condenser :  'Condenser',
    poweredCondenser :  'Powered Condenser',
    border : 'Border',
    switch : 'Switch',
    waterDetector: 'Water Detector',
    steamDetector: 'Steam Detector',
    inverter: "Inverter",
    jumper: "Jumper",
    pjumper: "Powered Jumper",
    ljumper: "Long Jumper",
    pljumper: "Powered Long Jumper",
    lightoff: "Light",
    lighton: "Light On",
    }
seq ={
   0: 0,
   1: 1,
   2: 8,
   3: 14,
   4: 17,
   5: 18,
   6: 20,
   7: 22,
   8: 11,
   9: 3,
   10: 2,
   11: 10,
   12: 4,
   13: 7,
   14: 5,
   15: 6,
   16: 16,
   17: 15,
   18: 9,
   19: 19,
   20: 12,
   21: 21,
   22: 13,
   23: 23
   }


def Exit():
   global RUNNING
   RUNNING = False
   
class Option:

    hovered = False
    
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.set_rect()
        self.draw()
            
    def draw(self):
        self.set_rend()
        DISPLAY.blit(self.rend, self.rect)
        
    def set_rend(self):
        self.rend = txtFont.render(self.text, True, self.get_color())
        
    def get_color(self):
        if self.hovered:
            return (0, 255, 0)
        else:
            return (0, 0, 255)
        
    def set_rect(self):
        self.set_rend()
        self.rect = self.rend.get_rect()
        self.rect.topleft = self.pos
        
    def work(self):
        global scroll_y
        if self.text =="Clear":
            game_engine.clearMap()
        elif self.text =="Load":
            game_engine.loadMap(seq[scroll_y])
        elif self.text == "Save":  
            game_engine.saveMap(seq[scroll_y])
        elif self.text =="Exit":
            Exit()
            
        
options = [Option("Clear", (20, Y*Square+40)), Option("Load", (320, Y*Square+40)),
           Option("Save", (520, Y*Square+40)), Option("Exit", (720, Y*Square+40))]



def gameStart():
    global RUNNING
    paused = True
    clickdown = False
    global scroll_y
    blokelis = 0
    FPS = 20
    pygame.init()
    iserasing = False
    i = -1

    

    while RUNNING:
        i = -1
        for event in pygame.event.get():
            if event.type == QUIT:
                RUNNING = False
                event.type
            elif event.type == pygame.KEYDOWN:
               clickdown = False
               if event.key == pygame.K_SPACE:
                  paused = not paused
               elif event.key == pygame.K_1:
                  FPS = 1
               elif event.key == pygame.K_2:
                  FPS = 3
               elif event.key == pygame.K_3:
                  FPS = 10
               elif event.key == pygame.K_4:
                  FPS = 20
               elif event.key == pygame.K_5:
                  FPS = 40
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button in [4,5,1]:
                for optione in options:
                    if optione.rect.collidepoint(pygame.mouse.get_pos()):
                        optione.work()
                if event.button == 4:
                    if scroll_y <23 :
                        scroll_y = max(scroll_y +1, 0)
                elif event.button == 5:
                    if scroll_y >0 :
                        scroll_y = min(scroll_y -1, 23)
                else : clickdown = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button ==1:
                clickdown = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                iserasing = True
                clickdown = False
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                iserasing = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
                tip = game_engine.returnblock([event.pos[0]//Square,event.pos[1]//Square])
                for k, v in seq.items():
                   if tip == v or isinstance(v, list) and tip in v:
                      scroll_y = k
                  
                   

        DISPLAY.fill((0,0,0)) 

        if paused:
           game_engine.updateMap()
        if iserasing and event.pos[1]<Square*Y:
           try:
              game_engine.changeblock([event.pos[0]//Square,event.pos[1]//Square],0)
           except Exception:
              pass
        if clickdown and event.pos[1]<Square*Y:
            try:
                game_engine.changeblock([event.pos[0]//Square,event.pos[1]//Square],seq[scroll_y])
            except Exception:
                pass
        for x in range(X):    
            for y in range(Y):
                i = i+1  
                DISPLAY.blit(pictures[game_engine.cmap[i]],(x*Square,y*Square))
  
        
            invText = txtFont.render(str(txtl[seq[scroll_y]]),True,(200,200,200),(0,0,0))
            DISPLAY.blit(invText,(X*Square-345,Y*Square))
            DISPLAY.blit(pictures[seq[scroll_y]],(20,Y*Square+10))
        
        for option in options:
                if option.rect.collidepoint(pygame.mouse.get_pos()):
                    option.hovered = True
                else:
                    option.hovered = False
                option.draw()
          
        pygame.display.update()
        clock.tick(FPS)



