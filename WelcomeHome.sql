Drop table if exists ItemIn;
Drop table if exists Delivered;
Drop table if exists Act;
Drop table if exists PersonPhone;
Drop table if exists DonatedBy;
Drop table if exists Ordered;

Drop table if exists Piece;
Drop table if exists Item;
Drop table if exists Category;
Drop table if exists `Location`;
Drop table if exists Person;
Drop table if exists `Role`;


CREATE TABLE Category (
    mainCategory VARCHAR(50) NOT NULL,
    subCategory VARCHAR(50) NOT NULL,
    catNotes TEXT,
    PRIMARY KEY (mainCategory, subCategory)
);

CREATE TABLE Item (
    ItemID INT NOT NULL,
    quantityNum INT NOT NULL,
    iDescription TEXT,
    photo BLOB,
    color VARCHAR(20),
    isNew TINYINT(1) DEFAULT 1,
    hasPieces TINYINT(1),
    material VARCHAR(50),
    mainCategory VARCHAR(50) NOT NULL,
    subCategory VARCHAR(50) NOT NULL,
    PRIMARY KEY (ItemID, quantityNum),
    FOREIGN KEY (mainCategory, subCategory) REFERENCES Category(mainCategory, subCategory)
);

CREATE TABLE Person (
    userName VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    fname VARCHAR(50) NOT NULL,
    lname VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL,
    PRIMARY KEY (userName)
);

CREATE TABLE PersonPhone (
    userName VARCHAR(50) NOT NULL,
    phone VARCHAR(20) NOT NULL,
    PRIMARY KEY (userName, phone),
    FOREIGN KEY (userName) REFERENCES Person(userName)
);

CREATE TABLE DonatedBy (
    ItemID INT NOT NULL,
    userName VARCHAR(50) NOT NULL,
    quantityNum INT NOT NULL,
    donateDate DATE NOT NULL,
    PRIMARY KEY (ItemID, quantityNum, userName),
    FOREIGN KEY (ItemID, quantityNum) REFERENCES Item(ItemID, quantityNum),
    FOREIGN KEY (userName) REFERENCES Person(userName)
);

CREATE TABLE Role (
    roleID VARCHAR(20) NOT NULL,
    rDescription VARCHAR(100),
    PRIMARY KEY (roleID)
);

CREATE TABLE Act (
    userName VARCHAR(50) NOT NULL,
    roleID VARCHAR(20) NOT NULL,
    PRIMARY KEY (userName, roleID),
    FOREIGN KEY (userName) REFERENCES Person(userName),
    FOREIGN KEY (roleID) REFERENCES Role(roleID)
);

CREATE TABLE Location (
    roomNum INT NOT NULL,
    shelfNum INT NOT NULL, 
    shelf VARCHAR(20),
    shelfDescription VARCHAR(200),
    PRIMARY KEY (roomNum, shelfNum)
);

CREATE TABLE Piece (
    ItemID INT NOT NULL,
    pieceNum INT NOT NULL,
    pDescription VARCHAR(200),
    length INT NOT NULL, 
    width INT NOT NULL,
    height INT NOT NULL,
    roomNum INT NOT NULL,
    shelfNum INT NOT NULL, 
    pNotes TEXT,
    PRIMARY KEY (ItemID, pieceNum),
    FOREIGN KEY (ItemID) REFERENCES Item(ItemID),
    FOREIGN KEY (roomNum, shelfNum) REFERENCES Location(roomNum, shelfNum)
);

CREATE TABLE Ordered (
    orderID INT NOT NULL AUTO_INCREMENT,
    orderDate DATE NOT NULL,
    orderNotes VARCHAR(200),
    supervisor VARCHAR(50) NOT NULL,
    client VARCHAR(50) NOT NULL,
    PRIMARY KEY (orderID),
    FOREIGN KEY (supervisor) REFERENCES Person(userName),
    FOREIGN KEY (client) REFERENCES Person(userName)
);

CREATE TABLE ItemIn (
    ItemID INT NOT NULL,
    orderID INT NOT NULL,
    quantityNum INT NOT NULL,
    found BOOLEAN DEFAULT FALSE,
    status ENUM('Available', 'Holding', 'Delivered') DEFAULT 'Available',
    holdingRoomNum INT, 
    holdingShelfNum INT, 
    PRIMARY KEY (ItemID, quantityNum, orderID),
    FOREIGN KEY (ItemID, quantityNum) REFERENCES Item(ItemID, quantityNum),
    FOREIGN KEY (orderID) REFERENCES Ordered(orderID),
    FOREIGN KEY (holdingRoomNum, holdingShelfNum) REFERENCES Location(roomNum, shelfNum)
);


CREATE TABLE Delivered (
    userName VARCHAR(50) NOT NULL,
    orderID INT NOT NULL,
    status ENUM('Pending', 'In Transit', 'Delivered', 'Cancelled') NOT NULL,
    date DATE NOT NULL,
    PRIMARY KEY (userName, orderID),
    FOREIGN KEY (userName) REFERENCES Person(userName),
    FOREIGN KEY (orderID) REFERENCES Ordered(orderID)
);
