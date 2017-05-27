import pygame, sys, random
from pygame.locals import *
from game_variables import *



DISPLAY = pygame.display.set_mode((X*Square, Y*Square+80))


pygame.display.set_caption('Sandbox')

pictures = {
    air : pygame.transform.scale(pygame.image.load('pictures/air.png'),(Square,Square)),
    battery : pygame.transform.scale(pygame.image.load('pictures/battery.png'),(Square,Square)),
    brick: pygame.transform.scale(pygame.image.load('pictures/brick.png'),(Square,Square)),
    heat  : pygame.transform.scale(pygame.image.load('pictures/heat.png'),(Square,Square)),
    lava   : pygame.transform.scale(pygame.image.load('pictures/lava.png'),(Square,Square)),
    sand : pygame.transform.scale(pygame.image.load('pictures/sand.png'),(Square,Square)),
    steam     : pygame.transform.scale(pygame.image.load('pictures/steam.png'),(Square,Square)),
    water : pygame.transform.scale(pygame.image.load('pictures/water.png'),(Square,Square)),
    wire : pygame.transform.scale(pygame.image.load('pictures/wire.png'),(Square,Square)),
    heatingHeat :  pygame.transform.scale(pygame.image.load('pictures/heatingHeat.png'),(Square,Square)),
    poweredWire : pygame.transform.scale(pygame.image.load('pictures/poweredWire.png'),(Square,Square)),
    condenser :  pygame.transform.scale(pygame.image.load('pictures/condenser.png'),(Square,Square)),
    poweredCondenser :  pygame.transform.scale(pygame.image.load('pictures/poweredCondenser.png'),(Square,Square)),
    border :  pygame.transform.scale(pygame.image.load('pictures/border.png'),(Square,Square)),
    switch :  pygame.transform.scale(pygame.image.load('pictures/switch.png'),(Square,Square)),
    waterDetector :  pygame.transform.scale(pygame.image.load('pictures/waterDetector.png'),(Square,Square)),
    steamDetector :  pygame.transform.scale(pygame.image.load('pictures/steamDetector.png'),(Square,Square)),
    inverter :  pygame.transform.scale(pygame.image.load('pictures/inverter.png'),(Square,Square)),
    jumper :  pygame.transform.scale(pygame.image.load('pictures/jumper.png'),(Square,Square)),
    pjumper :  pygame.transform.scale(pygame.image.load('pictures/jumper.png'),(Square,Square)),
    ljumper :  pygame.transform.scale(pygame.image.load('pictures/longjumper.png'),(Square,Square)),
    pljumper :  pygame.transform.scale(pygame.image.load('pictures/longjumper.png'),(Square,Square)),
    lightoff :  pygame.transform.scale(pygame.image.load('pictures/lightoff.png'),(Square,Square)),
    lighton :  pygame.transform.scale(pygame.image.load('pictures/lighton.png'),(Square,Square))

    }


