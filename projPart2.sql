-- C.a

INSERT INTO Category (mainCategory, subCategory, notes)
VALUES ('furniture', 'sofa', 'sofa furnitures');

INSERT INTO Item (iDescription, photo, color, isNew, hasPieces, material)
VALUES ('two-piece yellow sofa', NULL, 'yellow', TRUE, TRUE, 'silk');

-- we assume item id = 1

INSERT INTO ItemCategory (mainCategory, subCategory, ItemID)
VALUES ('furniture', 'sofa', 1);

INSERT INTO Person (userName, password, fname, lname, email)
VALUES ('testUser123', 'passwd', 'test', 'User', 'testUser123@example.com');


INSERT INTO DonatedBy (ItemID, userName, donateDate)
VALUES (1, 'testUser123', CURDATE());

INSERT INTO Piece (ItemID, pieceNum, pDescription, length, width, height)
VALUES (1, 1, 'sofa body', 30, 20, 20),
       (1, 2, 'cushion', 5, 5, 5);
INSERT INTO Location (roomNum, shelfNum, shelf, shelfDescription)
VALUES (5,0,NULL,"test shelf");

INSERT INTO PieceIn (ItemID, pieceNum, roomNum, shelfNum, notes)
VALUES (1, 1, 5, 0, 'Stored in Room 5, no designated shelf'),
       (1, 2, 5, 0, 'Stored in Room 5, no designated shelf');

-- C.b

SELECT
    Piece.ItemID,
    ItemCategory.mainCategory,
    ItemCategory.subCategory,
    PieceIn.pieceNum,
    PieceIn.roomNum,
    PieceIn.shelfNum,
    PieceIn.notes,
    Item.iDescription AS itemDescription,
    Piece.pDescription AS pieceDescription,
    Piece.length,
    Piece.width,
    Piece.height,
    Location.shelfDescription,
    Location.shelf
FROM
    ItemIn NATURAL JOIN
    Piece NATURAL JOIN
    ItemCategory NATURAL JOIN
    PieceIn NATURAL JOIN
    Location NATURAL JOIN
    Item
WHERE
    ItemIn.orderID = 12345;