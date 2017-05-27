import pygame, sys, random, pickle
from pygame.locals import *
import game_variables as data
X = data.X
Y = data.Y
def itc(integer):
    xlane = integer//Y
    ylane = integer-xlane*Y
    return([xlane,ylane])

def cti(temlist):
    xlane = temlist[0]*Y+temlist[1]
    return xlane
def changeblock(ylane, temtype):
    global cmap
    if cmap[cti(ylane)] != 13:
        cmap[cti(ylane)] = temtype
def returnblock(ylane):
    return cmap[cti(ylane)]
   

SIZE = X*Y
cmap = []
for i in range(SIZE):
    cmap.append(0)

for x in range (X):
    cmap[cti([x,Y-1])] = 13
    cmap[cti([x,0])] = 13
    
for y in range (Y):
    cmap[cti([0,y])] = 13
    cmap[cti([X-1,y])] = 13
blank = []
blank = cmap[:]
oldmap = []
oldmap = cmap[:]
def clearMap():
    global cmap
    global oldmap
    cmap = blank[:]
    oldmap = blank[:]

              
def saveMap(name):
    global cmap
    with open(str(name)+".txt", 'wb') as fp:
        pickle.dump(cmap, fp)

def loadMap(name):
    global cmap
    try:
        with open (str(name)+".txt", 'rb') as fp:
            itemlist = pickle.load(fp)
            cmap = itemlist[:]
    except Exception:
                pass

def PowerCloser(coord):     #Turns off circuits
    global cmap
    global oldmap
    x = coord[0]
    y = coord[1]
    for i in range(-1,2):
        for z in range(-1,2):
            if i == 1 and z == 1:
                continue
            if i == -1 and z == 1:
                continue
            if i == 1 and z == -1:
                continue
            if i == -1 and z == -1:
                continue
            
            try:
                if cmap[cti([x+i,y+z])] == 10: #wire
                    cmap[cti([x+i,y+z])] = 8
                    nx = x+i
                    ny = y+z
                    PowerCloser([nx,ny])
                elif cmap[cti([x+i,y+z])] == 9:#heat
                    cmap[cti([x+i,y+z])] = 3
                elif cmap[cti([x+i,y+z])] == 23:#LIGHT
                    cmap[cti([x+i,y+z])] = 22
                elif cmap[cti([x+i,y+z])] == 12:#condenser
                    cmap[cti([x+i,y+z])] = 11
                elif cmap[cti([x+i,y+z])] == 14:#switch
                    if [i,z] == [1,0] or [i,z] == [0,-1]:
                            if cmap[cti([x+i+1,y+z])] == 10:
                                cmap[cti([x+i+1,y+z])] =8
                                nx = x+i+1
                                ny = y+z
                                PowerCloser([nx,ny])
                            if cmap[cti([x+i,y+z-1])] == 10:
                                cmap[cti([x+i,y+z-1])] =8
                                nx = x+i
                                ny = y+z-1
                                PowerCloser([nx,ny])
                        
                elif cmap[cti([x+i,y+z])] == 17 and [i,z]==[1,0]: 

                        cmap[cti([x+i+1,y+z])] = 10
                        PowerSpider([x+i+1,y+z])
                elif cmap[cti([x+i,y+z])] == 19: #Jumper
                    cmap[cti([x+i,y+z])] = 18
                    if cmap[cti([x+(i*5),y+(z*5)])] == 10:
                        cmap[cti([x+(i*5),y+(z*5)])] = 8
                        nx = x+(i*5)
                        ny = y+(z*5)
                        PowerCloser([nx,ny])

                elif cmap[cti([x+i,y+z])] == 21: #long Jumper
                    cmap[cti([x+i,y+z])] = 20
                    if cmap[cti([x+(i*9),y+(z*9)])] == 10:
                        cmap[cti([x+(i*9),y+(z*9)])] = 8
                        PowerCloser([x+(i*9),y+(z*9)])


                               
            except Exception:
                pass
def PowerSpider(coord):                     #Powering all connected circuits
    global cmap
    global oldmap
    
    x = coord[0]
    y = coord[1]
    for i in range(-1,2):
        for z in range(-1,2):
            if i == 1 and z == 1:
                continue
            if i == -1 and z == 1:
                continue
            if i == 1 and z == -1:
                continue
            if i == -1 and z == -1:
                continue
            
            try:
                if cmap[cti([x+i,y+z])] == 8: #wire
                    cmap[cti([x+i,y+z])] = 10
                    nx = x+i
                    ny = y+z
                    PowerSpider([nx,ny])
                elif cmap[cti([x+i,y+z])] == 3:#heat
                    cmap[cti([x+i,y+z])] = 9
                elif cmap[cti([x+i,y+z])] == 11:#condenser
                    cmap[cti([x+i,y+z])] = 12
                elif cmap[cti([x+i,y+z])] == 22:    #light
                    cmap[cti([x+i,y+z])] = 23
                elif cmap[cti([x+i,y+z])] == 14:#switch

                    if [i,z] == [1,0] or [i,z] == [0,-1]:

                        if cmap[cti([x+i-1,y+z])] == 10 and cmap[cti([x+i,y+z+1])] == 10: 
                            if cmap[cti([x+i+1,y+z])] == 8:
                                cmap[cti([x+i+1,y+z])] =10
                                nx = x+i+1
                                ny = y+z
                                PowerSpider([nx,ny])

                            if cmap[cti([x+i,y+z-1])] == 8:
                                cmap[cti([x+i,y+z-1])] =10
                                nx = x+i
                                ny = y+z-1
                                PowerSpider([nx,ny])                             
                        
                elif cmap[cti([x+i,y+z])] == 17 and [i,z]==[1,0]: 
                    if cmap[cti([x+i+1,y+z])] == 10:
                        cmap[cti([x+i+1,y+z])] = 8
                        PowerCloser([x+i+1,y+z])

                elif cmap[cti([x+i,y+z])] == 18: #Jumper\
                    cmap[cti([x+i,y+z])] = 19
                    if cmap[cti([x+(i*5),y+(z*5)])] == 8:
                        cmap[cti([x+(i*5),y+(z*5)])] = 10
                        PowerSpider([x+(i*5),y+(z*5)])

                elif cmap[cti([x+i,y+z])] == 20: #Jumper
                    cmap[cti([x+i,y+z])] = 21
                    if cmap[cti([x+(i*7),y+(z*7)])] == 8:
                        cmap[cti([x+(i*7),y+(z*7)])] = 10
                        PowerSpider([x+(i*7),y+(z*7)])                                    
                               
            except Exception:
                pass

def updateMap():
    global cmap
    global oldmap
    
    for x in range(X):      #Turns off everything
        for y in range(Y):
            k = cti([x,y])
            if cmap[k] == 9:
                cmap[k] = 3
            elif cmap[k] == 10:
                cmap[k] = 8
            elif cmap[k] == 12:
                cmap[k] = 11
            elif cmap[k] == 19:
                cmap[k] = 18
            elif cmap[k] == 21:
                cmap[k] = 20
            elif cmap[k] == 23:
                cmap[k] = 22
    oldmap = cmap[:]
    for x in range(X):
        for y in range(Y):
            k = cti([x,y])
            if oldmap[k] == 17: #Inverter
                try:
                    if cmap[cti([x-1,y])] == 8:
                        if cmap[cti([x+1,y])] ==8:
                            cmap[cti([x+1,y])] =10
                            PowerSpider([x+1,y])
                except Exception:
                    pass
            elif oldmap[k] == 1:          #Battery
                for i in range(-1,2):
                    for z in range(-1,2):
                        if i == 0 and z == 0:
                            continue
                        try:
                            if cmap[cti([x+i,y+z])] == 8:
                                cmap[cti([x+i,y+z])] = 10
                                nx = x+i
                                ny = y+z
                                PowerSpider([nx,ny])
                            
                        except Exception:
                            pass
            elif oldmap[k] == 15: #Water detector
                on = False
                for i in range(-1,2):
                    for z in range(-1,2):
                        if i == 0 and z == 0:
                            continue
                        try:
                            if cmap[cti([x+i,y+z])] == 7:
                                on = True 
                        except Exception:
                            pass
                if on:
                   for i in range(-1,2):
                    for z in range(-1,2):
                        if i == 0 and z == 0:
                            continue
                        try:
                            if cmap[cti([x+i,y+z])] == 8:
                                cmap[cti([x+i,y+z])] = 10
                                nx = x+i
                                ny = y+z
                                PowerSpider([nx,ny])
                            
                        except Exception:
                            pass
            elif oldmap[k] == 16:
                on = False
                for i in range(-1,2):
                    for z in range(-1,2):
                        if i == 0 and z == 0:
                            continue
                        try:
                            if cmap[cti([x+i,y+z])] == 6:
                                on = True 
                        except Exception:
                            pass
                if on:
                   for i in range(-1,2):
                    for z in range(-1,2):
                        if i == 0 and z == 0:
                            continue
                        try:
                            if cmap[cti([x+i,y+z])] == 8:
                                cmap[cti([x+i,y+z])] = 10
                                nx = x+i
                                ny = y+z
                                PowerSpider([nx,ny])
                            
                        except Exception:
                            pass                          
            
    for x in range(X):
        for y in range(Y):
            k = cti([x,y])
            if oldmap[k] == 4 and cmap[k] == 4:      #Lava       
                if cmap[k+1] == 0:
                    cmap[k+1] = 4
                    cmap[k] = 0
                elif cmap[k+1] == 6:
                    cmap[k+1] = 4
                    cmap[k] = 6
                elif cmap[k+1] == 7:

                    cmap[k+1] = 2
                    oldmap[k+1] = 2
                    cmap[k] = 0
                
                
                elif cmap[cti([x-1,y])] == 0 and cmap[cti([x-1,y+1])] == 0:
                    cmap[cti([x-1,y+1])] = 4
                    cmap[k] = 0
                elif cmap[cti([x+1,y])] == 0 and cmap[cti([x+1,y+1])] == 0:
                    cmap[cti([x+1,y+1])] = 4
                    cmap[k] = 0
                elif cmap[cti([x-1,y])] == 6 and cmap[cti([x-1,y+1])] == 6:
                    cmap[cti([x-1,y+1])] = 4
                    cmap[k] = 6
                elif cmap[cti([x+1,y])] == 6 and cmap[cti([x+1,y+1])] == 6:
                    cmap[cti([x+1,y+1])] = 4
                    cmap[k] = 6
                elif cmap[cti([x-1,y])] == 6 and cmap[cti([x-1,y+1])] == 6 and oldmap[cti([x-1,y+1])] == 6 and oldmap[cti([x-1,y+1])] == 6:
                    if cmap[cti([x-1,y-1])] != 4 and cmap[cti([x-1,y-1])] != 0 and cmap[cti([x-1,y-1])] != 7:  
                        cmap[cti([x-1,y+1])] = 4
                        cmap[k] = 6
                elif cmap[cti([x+1,y])] == 6 and cmap[cti([x+1,y+1])] == 6 and oldmap[cti([x+1,y+1])] == 6 and oldmap[cti([x+1,y+1])] == 6:
                    if cmap[cti([x+1,y-1])] != 7 and cmap[cti([x+1,y-1])] != 0 and cmap[cti([x+1,y-1])] != 4:
                        cmap[cti([x+1,y+1])] = 4
                        cmap[k] = 6
                else:
                    find = False
                    for i in range(-1,2):
                        if find:
                            break
                        for z in range(-1,2):
                            if i == 0 and z == 0:
                                continue
                            if i == -1 and z == -1:
                                continue
                            if i == 1 and z == -1:
                                continue
                            if i == 0 and z == -1:
                                continue
                            try:
                                if cmap[cti([x+i,y+z])] == 0: 
                                    cmap[cti([x+i,y+z])] = 4
                                    cmap[k] = 0
                                    find = True
                                    break
                                elif cmap[cti([x+i,y+z])] == 6 and oldmap[cti([x+i,y+z])] == 0:
                                    cmap[cti([x+i,y+z])] = 4
                                    cmap[k] = 6
                                    find = True
                                    break
                                elif cmap[cti([x+i,y+z])] == 7: 
                                    cmap[cti([x+i,y+z])] = 2
                                    cmap[k] = 0
                                    find = True
                                    break

                                elif cmap[cti([x+i,y+z])] == 6 and oldmap[cti([x+i,y+z])] == 6:
                                    if cmap[cti([x+i,y+z-1])] != 7 and cmap[cti([x+i,y+z-1])] != 6 and cmap[cti([x+i,y+z-1])] != 4 and cmap[cti([x+i,y+z-1])] != 0: 
                                        cmap[cti([x+i,y+z])] = 4
                                        cmap[k] = 6
                                        find = True
                                        break
                            except Exception:
                                pass
                        
                      
                            

                            
            elif oldmap[k] == 5 and cmap[k] == 5:  #SAND
                if cmap[k+1] == 0 and oldmap[k+1] == 0:
                    cmap[k+1] = 5
                    cmap[k] = 0
                elif cmap[k+1] == 6 and oldmap[k+1] == 6:
                    cmap[k+1] = 5
                    cmap[k] = 6
                elif cmap[k+1] == 4 and oldmap[k+1] == 4:
                    cmap[k+1] = 5
                    cmap[k] = 4
                elif cmap[k+1] == 7 and oldmap[k+1] == 7:
                    cmap[k+1] = 5
                    cmap[k] = 7
                
                elif cmap[cti([x-1,y+1])] == 0:
                    cmap[cti([x-1,y+1])] = 5
                    cmap[k] = 0
                elif cmap[cti([x-1,y+1])] == 4:
                    cmap[cti([x-1,y+1])] = 5
                    cmap[k] = 4
                elif cmap[cti([x-1,y+1])] == 7:
                    cmap[cti([x-1,y+1])] = 5
                    cmap[k] = 7
                elif cmap[cti([x-1,y+1])] == 6:
                    cmap[cti([x-1,y+1])] = 5
                    cmap[k] = 6
                elif cmap[cti([x+1,y+1])] == 0:
                    cmap[cti([x+1,y+1])] = 5
                    cmap[k] = 0
                elif cmap[cti([x+1,y+1])] == 4:
                    cmap[cti([x+1,y+1])] = 5
                    cmap[k] = 4
                elif cmap[cti([x+1,y+1])] == 7:
                    cmap[cti([x+1,y+1])] = 5
                    cmap[k] = 7
                elif cmap[cti([x+1,y+1])] == 6:
                    cmap[cti([x+1,y+1])] = 5
                    cmap[k] = 6
                else:
                    find = False
                    for i in range(-1,2):
                        if find:
                            break
                        try:
                            if cmap[cti([x+i,y+1])] == 0:
                                cmap[cti([x+i,y+1])] = 5
                                cmap[k] = 0
                                find = True
                                break
                            elif cmap[cti([x+i,y+1])] == 4:
                                cmap[cti([x+i,y+1])] = 5
                                cmap[k] = 4
                                find = True
                                break
                            elif cmap[cti([x+i,y+1])] == 6:
                                cmap[cti([x+i,y+1])] = 5
                                cmap[k] = 6
                                find = True
                                break
                            elif cmap[cti([x+i,y+1])] == 7:
                                cmap[cti([x+i,y+1])] = 5
                                cmap[k] = 7
                                find = True
                                break
                        except Exception:
                            pass
            elif oldmap[k] == 6 and cmap[k] ==6:          #STEAM
                if cmap[k-1] == 0:
                    cmap[k-1] = 6
                    cmap[k] =0
                elif cmap[k-1] == 4 and oldmap[k-1] == 4:
                    cmap[k-1] = 6
                    cmap[k] =4
                elif cmap[k-1] == 5 and oldmap[k-1] == 5:
                    cmap[k-1] = 6
                    cmap[k] =5
                elif cmap[k-1] == 7 and oldmap[k-1] == 7:
                    cmap[k-1] = 6
                    cmap[k] =7
                else:
                    find = False
                    for i in range(-1,2):
                        if find:
                            break
                        for z in range(-1,1):
                            if i == 0 and z == 0:
                                continue
                            try:
                                if cmap[cti([x+i,y+z])] == 0:
                                    cmap[cti([x+i,y+z])] = 6
                                    cmap[k] = 0
                                    find = True
                                    break
                            except Exception:
                                pass
            elif oldmap[k] == 7 and cmap[k] == 7:          #WATER
                if cmap[k+1] ==0:
                    cmap[k+1] = 7
                    cmap[k] = 0
                elif cmap[k+1] == 4:
                    cmap[k+1] = 6
                    cmap[k] = 0
                elif cmap[k+1] == 6:
                    cmap[k+1] = 7
                    cmap[k] = 6
                elif cmap[cti([x-1,y])] == 0 and cmap[cti([x-1,y+1])] == 0:
                    cmap[cti([x-1,y+1])] = 7
                    cmap[k] = 0
                elif cmap[cti([x+1,y])] == 0 and cmap[cti([x+1,y+1])] == 0:
                    cmap[cti([x+1,y+1])] = 7
                    cmap[k] = 0
                elif cmap[cti([x-1,y])] == 6 and cmap[cti([x-1,y+1])] == 6 and oldmap[cti([x-1,y+1])] == 6 and oldmap[cti([x-1,y+1])] == 6:
                    if cmap[cti([x-1,y-1])] != 7 and cmap[cti([x-1,y-1])] != 0 and cmap[cti([x-1,y-1])] != 4:  
                        cmap[cti([x-1,y+1])] = 7
                        cmap[k] = 6
                elif cmap[cti([x+1,y])] == 6 and cmap[cti([x+1,y+1])] == 6 and oldmap[cti([x+1,y+1])] == 6 and oldmap[cti([x+1,y+1])] == 6:
                    if cmap[cti([x+1,y-1])] != 7 and cmap[cti([x+1,y-1])] != 0 and cmap[cti([x+1,y-1])] != 4:
                        cmap[cti([x+1,y+1])] = 7
                        cmap[k] = 6
                    
    
                else:
                    find = False
                    for i in range(-1,2):
                        if find:
                            break
                        for z in range(0,2):
                            if i == 0 and z == 0:
                                continue
                            try:
                                if cmap[cti([x+i,y+z])] == 0: 
                                    cmap[cti([x+i,y+z])] = 7
                                    cmap[k] = 0
                                    find = True
                                    break
                                elif cmap[cti([x+i,y+z])] == 4: 
                                    cmap[cti([x+i,y+z])] = 6
                                    cmap[k] = 0
                                    find = True
                                    break
                                elif cmap[cti([x+i,y+z])] == 6 and oldmap[cti([x+i,y+z])] == 6:
                                    if cmap[cti([x+i,y+z-1])] != 7 and cmap[cti([x+i,y+z-1])] != 6 and cmap[cti([x+i,y+z-1])] != 4 and cmap[cti([x+i,y+z-1])] != 0: 
                                        cmap[cti([x+i,y+z])] = 7
                                        cmap[k] = 6
                                        find = True
                                        break
                            except Exception:
                                pass
            elif cmap[k] == 9:      #POWERED HEATER
                for i in range(-1,2):
                    for z in range(-1,2):
                        if i == 0 and z == 0:
                            continue
                        if i == 1 and z == 1:
                            continue
                        if i == -1 and z == 1:
                            continue
                        if i == 1 and z == -1:
                            continue
                        if i == -1 and z == -1:
                            continue
                        try:
                            if cmap[cti([x+i,y+z])] == 7:
                                cmap[cti([x+i,y+z])] = 6
                        except Exception:
                            pass
            elif cmap[k] == 12:      #POWERED CONDENSER
                for i in range(-1,2):
                    for z in range(-1,2):
                        if i == 0 and z == 0:
                            continue
                        if i == 1 and z == 1:
                            continue
                        if i == -1 and z == 1:
                            continue
                        if i == 1 and z == -1:
                            continue
                        if i == -1 and z == -1:
                            continue
                        try:
                            if cmap[cti([x+i,y+z])] == 6:

                                cmap[cti([x+i,y+z])] = 7

                        except Exception:
                            pass
                                                                                         




