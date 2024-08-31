import pygame
import time
import helper

def main():
    pygame.init()

    ## Game Window
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Drag And Drop')

    ## Background Image
    fridgeImg = pygame.image.load('./images/background/refrigerator .jpg')
    pantryImg = pygame.image.load('./images/background/pantry(bright).jpg')
    dpantryImg = pygame.image.load('./images/background/pantry(dark).jpg')
    fridgeImg = pygame.transform.scale(fridgeImg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    pantryImg = pygame.transform.scale(pantryImg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    dpantryImg = pygame.transform.scale(dpantryImg, (SCREEN_WIDTH, SCREEN_HEIGHT))
    currentBgd = fridgeImg

    ## Display Game Instructions
    smallFont = pygame.font.Font('freesansbold.ttf', 16)
    locChangeDisplay = smallFont.render('Press P to change location', True, (0, 0, 128))
    locChangeRect = locChangeDisplay.get_rect()
    locChangeRect.centerx = SCREEN_WIDTH // 2

    ## Display Information
    bigFont = pygame.font.Font('freesansbold.ttf', 36)
    infoText = ""
    MAX_WIDTH = 800

    # Timing to Display Information
    showStartTime = None
    infoDelay = 5

    ## List of Pieces (Can Drag)
    pieces = helper.loadPieces(fridgeImg, pantryImg, dpantryImg)
    active_piece = None # no box is being clicked

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for piece in pieces:
                    if piece.getRect().collidepoint(event.pos):
                        active_piece = piece

            if event.type == pygame.MOUSEBUTTONUP:
                if active_piece != None:
                    if (active_piece.getTarget().colliderect(active_piece.getRect()) and # Piece placed in target position
                            currentBgd == active_piece.getTargetBgd()):
                        pieces.pop(active_piece.index) # Remove from list -> Removes from screen
                        infoText = active_piece.getInfo()
                        showStartTime = time.time() # Time of putting object right
                    active_piece = None # No longer holding onto any piece


            if event.type == pygame.MOUSEMOTION:
                if active_piece != None:
                    active_piece.getRect().move_ip(event.rel)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    # Change background when 'P' is pressed
                    if currentBgd == fridgeImg:
                        currentBgd = pantryImg
                    elif currentBgd == pantryImg:
                        currentBgd = dpantryImg
                    else:
                        currentBgd = fridgeImg

            if event.type == pygame.QUIT: # User closed the window
                run = False

        ## Draw Everything
        currentTime = time.time()
        
        screen.blit(currentBgd, (0, 0))
        screen.blit(locChangeDisplay, locChangeRect) # Instructions

        ## Display Information after successfully placing a piece
        if showStartTime and currentTime - showStartTime <= infoDelay:
            wrapped_lines = helper.wrapText(infoText, bigFont, MAX_WIDTH)
            
            ## Draw Wrapped Text
            y_offset = 200
            for line in wrapped_lines:
                infoDisplay = bigFont.render(line, True, (0, 0, 0))
                screen.blit(infoDisplay, (200, y_offset))
                y_offset += infoDisplay.get_height() + 32

            if len(pieces) == 0: # All pieces have been put correctly
                run = False
                pygame.quit()
                return # Exit Pygame

        else:
            infoText = "" # Clear message after delay
            showStartTime = None

        for piece in pieces: # Draw pieces
            screen.blit(piece.getImage(), piece.getRect())
            # if piece.index == 7: # for debugging
            #     pygame.draw.rect(screen, (0,0,0), piece.getTarget()) 
        
        pygame.display.flip()
        pygame.time.Clock().tick(60) # Cap the frame rate