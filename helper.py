import pygame

class Piece:
    
    def __init__(self, i, png, x, y):
        self.index = i

        self.image = pygame.image.load(f'./images/food/{png}')
        self.rect = self.image.get_rect()
        self.target = pygame.Rect(x, y, self.rect.width, self.rect.height)

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
    
    def setInfo(self, info):
        self.info = info
    
def loadPieces(fridge, pantry, dpantry):
    pieces = []

    # Open the file for reading
    with open('foodloop.txt', 'r') as file:
        # Read all lines in the file
        lines = file.readlines()

    # Process each line
    for line in lines:
        line = line.strip() # Strip any leading/trailing whitespace characters (like newlines)
        var = line.split(',') # Split the line by commas
        # Print the resulting list of variables
        pieces.append(Piece(int(var[0]), var[1], int(var[2]), int(var[3]))) #id, jpg, x, y

    ## Set Description
    with open ('desc.txt', 'r') as f:
        lines = f.readlines()

    ## Process each line
    for num, line in enumerate(lines):
        line = line.strip()
        pieces[num].setInfo(line)

    ## Set Target Location
    for i in range(7):
        pieces[i].setTargetBgd(fridge)

    for i in range(7, 12):
        pieces[i].setTargetBgd(dpantry)

    for i in range(12, 15):
        pieces[i].setTargetBgd(pantry)
    
    return pieces

def wrapText(text, font, max_width):
    """Wrap text for a given width using the specified font."""
    words = text.split(' ')
    lines = []
    current_line = ''
    
    for word in words:
        # Create a line of text including the new word
        test_line = f'{current_line} {word}'.strip()
        # Measure the width of the text
        test_surface = font.render(test_line, True, (0, 0, 0))
        test_width = test_surface.get_width()
        
        if test_width <= max_width:
            # If the line fits, add the word to the current line
            current_line = test_line
        else:
            # Otherwise, add the current line to the list and start a new line
            lines.append(current_line)
            current_line = word
    
    # Add the last line
    if current_line:
        lines.append(current_line)
    
    return lines