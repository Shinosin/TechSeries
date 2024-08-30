import pygame

class Piece:
    
    def __init__(self, i, jpg, x, y, bgd, info):
        self.index = i

        self.image = pygame.image.load(f'./images/{jpg}')
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.target = pygame.Rect(x, y, self.rect.width, self.rect.height)
        self.targetBgd = bgd
        self.info = info

    def getRect(self):
        return self.rect
    
    def getTarget(self):
        return self.target
    
    def getTargetBgd(self):
        return self.targetBgd
    
    def getInfo(self):
        return self.info
    
    def getImage(self):
        return self.image