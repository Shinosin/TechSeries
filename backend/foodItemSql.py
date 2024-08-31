# Created foodItem table
CREATE_FOODITEM = '''
CREATE TABLE IF NOT EXISTS foodItem (
    id INTEGER PRIMARY KEY NOT NULL AUTO_INCREMENT,
    foodItemName TEXT NOT NULL ,
    expiryDate DATE 
);
'''

## sql insert statements ##
INSERT_FOODITEM = '''
    INSERT INTO foodItem(
        foodItemName, expiryDate
    ) 
    VALUES(
        :foodItemName, :expiryDate
    );
'''