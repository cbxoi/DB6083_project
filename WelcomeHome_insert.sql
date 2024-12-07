delete from Person;
delete from `Role`;
delete from Act;
delete from Item;
delete from DonatedBy;
delete from Category;
delete from Piece;
delete from `Location`;
delete from Ordered;
delete from ItemIn;
delete from PersonPhone;
delete from Delivered;

INSERT INTO Category (mainCategory, subCategory, catNotes)
VALUES
    ('Furniture', 'Tables', 'Tables for dining and working'),
    ('Furniture', 'Chairs', 'Various types of chairs'),
    ('Electronics', 'Laptops', 'Portable computers');

INSERT INTO Item (ItemID, quantityNum, iDescription, color, isNew, hasPieces, material, mainCategory, subCategory)
VALUES
    (1001, 1, 'Wooden dining table', 'Brown', 1, 1, 'Wood', 'Furniture', 'Tables'),
    (1002, 2, 'Ergonomic office chair', 'Black', 1, 0, 'Plastic', 'Furniture', 'Chairs'),
    (1003, 1, 'Gaming laptop', 'Silver', 1, 0, 'Metal', 'Electronics', 'Laptops');

INSERT INTO Person (userName, password, fname, lname, email)
VALUES
    ('test1', '123', 'Buxiao', 'Chu', 'bc3730@nyu.com'),
    ('test2', '123', 'Xingyu', 'Xian', 'bc3730@nyu.com'),
    ('test3', '123', 'Yibo', 'Zhang', 'yz10589@nyu.com');

INSERT INTO PersonPhone (userName, phone)
VALUES
    ('test1', '123-456-7890'),
    ('test2', '987-654-3210'),
    ('test3', '555-666-7777');

INSERT INTO DonatedBy (ItemID, userName, quantityNum, donateDate)
VALUES
    (1001, 'test1', 1, '2024-10-01'),
    (1002, 'test2', 2, '2024-10-02'),
    (1003, 'test3', 3, '2024-10-03');

INSERT INTO Role (roleID, rDescription)
VALUES
    ('staff', 'Staff member responsible for managing orders'),
    ('volunteer', 'Volunteer assisting with order preparation'),
    ('client', 'Client receiving donated items');

INSERT INTO Act (userName, roleID)
VALUES
    ('test1', 'staff'),
    ('test2', 'volunteer'),
    ('test3', 'client');

INSERT INTO Location (roomNum, shelfNum, shelf, shelfDescription)
VALUES
    (1, 1, 'A1', 'Top shelf in room 1'),
    (1, 2, 'B1', 'Middle shelf in room 1'),
    (2, 1, 'C1', 'Top shelf in room 2');

INSERT INTO Piece (ItemID, pieceNum, pDescription, length, width, height, roomNum, shelfNum, pNotes)
VALUES
    (1001, 1, 'Table top', 100, 60, 5, 1, 1, 'Main part of the table'),
    (1001, 2, 'Table leg', 5, 5, 70, 1, 2, 'Leg of the table'),
    (1002, 1, 'Chair base', 40, 40, 10, 2, 1, 'Base of the chair');

INSERT INTO Ordered (orderDate, orderNotes, supervisor, client)
VALUES
    ('2024-10-05', 'Order for dining table', 'test1', 'test3'),
    ('2024-10-06', 'Order for office chair', 'test1', 'test3');

INSERT INTO ItemIn (ItemID, orderID, quantityNum, found)
VALUES
    (1001, 1, 1, FALSE),
    (1002, 2, 2, TRUE);

INSERT INTO Delivered (userName, orderID, status, date)
VALUES
    ('test2', 1, 'Delivered', '2024-10-07'),
    ('test2', 2, 'In Transit', '2024-10-08');