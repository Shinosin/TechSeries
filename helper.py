from piece import Piece

def correct(num):
    ## num references an item 
    ## rn apple = 0, fish = 1
    if num == 0: 
        return "That's right!"
    elif num == 1:
        return "FISHHSHHHH"
    
def loadPieces(fridge, pantry):
    # for i in range(2): # 2 Objects total
    ###### CONSDIER USING CSV
    apple = Piece(0, 'apple.jpg', 300, 300, pantry)
    fish = Piece(1, "fish.jpg", 700, 700, fridge)

    return []