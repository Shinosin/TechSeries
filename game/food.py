class Food:
    
    def __init__(self, name, ):
        self.name = name

    def display(self):
        print(self.name)


food = Food("apple")
food.display()