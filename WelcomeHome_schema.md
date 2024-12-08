# Project WelcomeHome Schema

### Category
Category(**mainCategory**, **subCategory**, catNotes)

### Item
Item(**ItemID**, **quantityNum**, iDescription, photo, color, isNew, hasPieces, material, mainCategory, subCategory)  
Item(mainCategory, subCategory) REFERENCES Category(mainCategory, subCategory)

### Person
Person(**userName**, password, fname, lname, email)

### PersonPhone
PersonPhone(**userName**, **phone**)  
PersonPhone(userName) REFERENCES Person(userName)

### DonatedBy
DonatedBy(**ItemID**, **quantityNum**, **userName**, donateDate)  
DonatedBy(ItemID, quantityNum) REFERENCES Item(ItemID, quantityNum)  
DonatedBy(userName) REFERENCES Person(userName)

### Role
Role(**roleID**, rDescription)

### Act
Act(**userName**, **roleID**)  
Act(userName) REFERENCES Person(userName)  
Act(roleID) REFERENCES Role(roleID)

### Location
Location(**roomNum**, **shelfNum**, shelf, shelfDescription)

### Piece
Piece(**ItemID**, **pieceNum**, pDescription, length, width, height, roomNum, shelfNum, pNotes)  
Piece(ItemID) REFERENCES Item(ItemID)  
Piece(roomNum, shelfNum) REFERENCES Location(roomNum, shelfNum)

### Ordered
Ordered(**orderID**, orderDate, orderNotes, supervisor, client)  
Ordered(supervisor) REFERENCES Person(userName)  
Ordered(client) REFERENCES Person(userName)

### ItemIn
ItemIn(**ItemID**, **quantityNum**, **orderID**, found, status, holdingRoomNum, holdingShelfNum)  
ItemIn(ItemID, quantityNum) REFERENCES Item(ItemID, quantityNum)  
ItemIn(orderID) REFERENCES Ordered(orderID)  
ItemIn(holdingRoomNum, holdingShelfNum) REFERENCES Location(roomNum, shelfNum)

### Delivered
Delivered(**userName**, **orderID**, status, date)  
Delivered(userName) REFERENCES Person(userName)  
Delivered(orderID) REFERENCES Ordered(orderID)
