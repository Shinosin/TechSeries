import pygame

def loadImages():
    appleImg = pygame.image.load('apple.jpg')
    fishImg = pygame.image.load('fish.jpg')
    return [appleImg, fishImg]

def correct(num):
    ## num references an item 
    ## rn apple = 0, fish = 1
    if num == 0: 
        return "That's right!"
    elif num == 1:
        return "FISHHSHHHH"