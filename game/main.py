import pygame
import asyncio
import helper
import time

pygame.init()

## Game Window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Drag And Drop')

## Background Image
fridgeImg = pygame.image.load('fridge.jpg')  # Make sure the image path is correct
fridgeImg = pygame.transform.scale(fridgeImg, (SCREEN_WIDTH, SCREEN_HEIGHT))
pantryImg = pygame.image.load('pantry.jpg')
pantryImg = pygame.transform.scale(pantryImg, (SCREEN_WIDTH, SCREEN_HEIGHT))
currentBgd = fridgeImg

## Display Quit Instructions
smallFont = pygame.font.Font('freesansbold.ttf', 16)
locChangeDisplay = smallFont.render('Press P to change location', True, (0, 0, 128))
locChangeRect = locChangeDisplay.get_rect()
locChangeRect.centerx = SCREEN_WIDTH // 2

## Display Information
bigFont = pygame.font.Font('freesansbold.ttf', 72)

# Timing

## List of Images
images = helper.loadImages()

## Target Positions === consider backgrd img oso
appleLoc = pygame.Rect(50, 50, 153, 180)
fishLoc = pygame.Rect(200, 200, 180, 180)
targetLoc = [appleLoc, fishLoc]
# fishLoc = pygame.Rect(400, 200, images[1].width, images[1].height)

async def main():
    ## Var
    infoText = ""
    showStartTime = None
    infoDelay = 2
    currentBgd = fridgeImg
    endTime = None

    active_box = None # no box is being clicked
    boxes = []
    for i in range(len(images)):
        box = images[i].get_rect()
        boxes.append(box)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                for num, box in enumerate(boxes):
                    if box.collidepoint(event.pos):
                        active_box = (box, num)

            if event.type == pygame.MOUSEBUTTONUP:
                if active_box != None:

                    if (targetLoc[active_box[1]].colliderect(active_box[0]) and 
                            active_box[0] == boxes[active_box[1]]):

                        boxes.pop(active_box[1])
                        images.pop(active_box[1])
                        targetLoc.pop(active_box[1])
                        infoText = helper.correct(active_box[1])
                        showStartTime = time.time() # time of placing obj correctly
                    
                    active_box = None


            if event.type == pygame.MOUSEMOTION:
                if active_box != None:
                    boxes[active_box[1]].move_ip(event.rel)

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_p:
                    # Change background when 'P' is pressed
                    if currentBgd == fridgeImg:
                        currentBgd = pantryImg
                    else:
                        currentBgd = fridgeImg

                elif event.key == pygame.K_q: ### CAN DEL
                    run = False

        ## Draw Everything
        currentTime = time.time()
        
        screen.blit(currentBgd, (0, 0))
        screen.blit(locChangeDisplay, locChangeRect) # p instructions

        if showStartTime and currentTime - showStartTime <= infoDelay:
            infoDisplay = bigFont.render(infoText, True, (0, 0, 128))

            infoRect = infoDisplay.get_rect()
            infoRect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            screen.blit(infoDisplay, infoRect)

            if len(targetLoc) == 0: # Game over
                run = False 
            ## flask back to a page or smth

        else:
            infoText = ""
            showStartTime = None


        

        for i in range(len(images)):
            screen.blit(images[i], boxes[i])
        #update and draw items
        # for box in boxes:
        #     screen.blit(appleimg, box)
            # pygame.draw.rect(screen, "purple", box) # draw clickable items

        pygame.display.flip()
        pygame.time.Clock().tick(60) # Cap the frame rate
        # pygame.display.update()
        await asyncio.sleep(0)

    pygame.quit()




asyncio.run(main())