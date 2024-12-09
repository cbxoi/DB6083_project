delete from Delivered;
delete from ItemIn;
delete from Ordered;
delete from PersonPhone;
delete from Act;
delete from DonatedBy;
delete from Piece;
delete from Item;

delete from Person;
delete from `Role`;
delete from Category;
delete from `Location`;

INSERT INTO Category (mainCategory, subCategory, catNotes)
VALUES
    ('Furniture', 'Tables', 'Tables for dining and working'),
    ('Furniture', 'Chairs', 'Various types of chairs'),
    ('Electronics', 'Laptops', 'Portable computers'),
    ('Toys', 'Building', 'Building toys for children'),
    ('Tools', 'Hand Tools', 'Hand tools for various tasks');

INSERT INTO Item (ItemID, quantityNum, iDescription, photo, color, isNew, hasPieces, material, mainCategory, subCategory)
VALUES
    (1001, 1, 'Toy 1', NULL, 'Red', 1, 0, 'Plastic', 'Toys', 'Building'),
    (1002, 2, 'Tool', NULL, 'Blue', 1, 0, 'Metal', 'Tools', 'Hand Tools'),
    (1003, 3, 'Chair', NULL, 'Green', 1, 0, 'Wood', 'Furniture', 'Chairs'),
    (1004, 4, 'laptop1', NULL, 'Black', 0, 0, 'Metal', 'Electronics', 'Laptops'),
    (1005, 5, 'laptop2', NULL, 'Silver', 1, 0, 'Metal', 'Electronics', 'Laptops');

INSERT INTO Person (userName, password, fname, lname, email)
VALUES
    ('test1', '123', 'Buxiao', 'Chu', 'bc3730@nyu.com'),
    ('test2', '123', 'Xingyu', 'Xian', 'xx2360@nyu.com'),
    ('test3', '123', 'Yibo', 'Zhang', 'yz10589@nyu.com'),
    ('test4', '123', 'Jack', 'Black', 'jackblack@gmail.com');

INSERT INTO PersonPhone (userName, phone)
VALUES
    ('test1', '123-456-7890'),
    ('test2', '987-654-3210'),
    ('test3', '555-666-7777'),
    ('test4', '111-222-3333');

INSERT INTO DonatedBy (ItemID, userName, quantityNum, donateDate)
VALUES
    (1001, 'test4', 1, '2024-10-01'),
    (1002, 'test4', 2, '2024-10-02'),
    (1003, 'test4', 3, '2024-10-03'),
    (1004, 'test4', 2, '2024-10-04'),
    (1005, 'test4', 2, '2024-10-05');

INSERT INTO Role (roleID, rDescription)
VALUES
    ('staff', 'Staff member responsible for managing orders'),
    ('volunteer', 'Volunteer assisting with order preparation'),
    ('client', 'Client receiving donated items'),
    ('donor', 'Donor contributing items to the organization');

INSERT INTO Act (userName, roleID)
VALUES
    ('test1', 'staff'),
    ('test2', 'volunteer'),
    ('test3', 'client'),
    ('test4', 'donor');

INSERT INTO Location (roomNum, shelfNum, shelf, shelfDescription)
VALUES
    (1, 1, 'A1', 'Top shelf in room 1'),
    (1, 2, 'B1', 'Middle shelf in room 1'),
    (2, 1, 'C1', 'Top shelf in room 2'),
    (99, 1, 'Holding', 'Holding area for items ready for delivery');


INSERT INTO Piece (ItemID, pieceNum, pDescription, length, width, height, roomNum, shelfNum, pNotes)
VALUES
    (1001, 1, 'Table top', 100, 60, 5, 1, 1, 'Main part of the table'),
    (1001, 2, 'Table leg', 5, 5, 70, 1, 2, 'Leg of the table'),
    (1002, 1, 'Chair base', 40, 40, 10, 2, 1, 'Base of the chair'),
    (1004, 1, 'Laptop', 30, 20, 5, 2, 1, 'Main part of the laptop'),
    (1005, 1, 'Laptop', 30, 20, 5, 2, 1, 'Main part of the laptop');

INSERT INTO Ordered (orderID, orderDate, orderNotes, supervisor, client)
VALUES
    (1, '2024-10-05', 'Order for dining table', 'test1', 'test3'),
    (2, '2024-10-06', 'Order for office chair', 'test1', 'test3'),
    (3, '2024-10-07', 'Order for laptop', 'test1', 'test3');

INSERT INTO ItemIn (ItemID, orderID, quantityNum, found, status, holdingRoomNum, holdingShelfNum)
VALUES
    (1001, 1, 1, 0, 'Holding', 99, 1),  
    (1002, 2, 2, 1, 'Available', 2, 1),
    (1004, 3, 2, 1, 'Available', 2, 1),
    (1005, 3, 2, 1, 'Available', 2, 1);

INSERT INTO Delivered (userName, orderID, status, date)
VALUES
    ('test2', 1, 'Delivered', '2024-10-07'),
    ('test2', 2, 'In Transit', '2024-10-08'),
    ('test2', 3, 'In Transit', '2024-10-09');
