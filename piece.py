import pygame

class Piece:
    
    def __init__(self, i, jpg, x, y, info):
        self.index = i

        self.image = pygame.image.load(f'./images/{jpg}')
        # self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.target = pygame.Rect(x, y, self.rect.width + 15, self.rect.height + 15) # Buffer
        self.info = info

    def setTargetBgd(self, location):
        self.targetBgd = location

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
    
def loadPieces(fridge, pantry):
    # for i in range(2): # 2 Objects total
    ###### CONSDIER USING CSV
    apple = Piece(0, 'apple.jpg', 300, 300, pantry, "apple is good")
    fish = Piece(1, "fish.jpg", 70, 70, fridge, "fish also good")
    
    ### USE THIS AFT TXT OBTAINED
    # pieces = []

    # # Open the file for reading
    # with open('pieces.txt', 'r') as file:
    #     # Read all lines in the file
    #     lines = file.readlines()

    # # Process each line
    # for line in lines:
    #     line = line.strip() # Strip any leading/trailing whitespace characters (like newlines)
    #     var = line.split(',') # Split the line by commas
    #     # Print the resulting list of variables
    #     pieces.append(Piece(int(var[0]), var[1], int(var[2]), int(var[3]), var[4])) #id, jpg, x, y, desc

    # ## Set Target Location
    # for i in range(5):
    #     pieces[i].setTargetLocation(pantry)
    
    # for i in range(6):
    #     pieces[i].setTargetLocation(fridge)

    return [apple, fish]