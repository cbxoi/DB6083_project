delete from Person;
delete from `Role`;
delete from Act;
delete from Item;
delete from DonatedBy;
delete from Category;
delete from ItemCategory;
delete from Piece;
delete from `Of`;
delete from `Location`;
delete from PieceIn;
delete from `Order`;
delete from ItemIn;
delete from `For`;
delete from Supervised;
delete from Delivered;

Insert into `Role` values ('1', 'staff');
Insert into `Role` values ('2', 'volunteer');
Insert into `Role` values ('3', 'client');
Insert into `Role` values ('4', 'donor');

-- C.a.
Insert into Person values ('BuxiaoChu1', 'password', 'Buxiao', 'Chu', 'bc3730@nyu.com');
Insert into Person values ('XingyuXian2', 'password', 'Xingyu', 'Xian', '');
Insert into Person values ('YiboZhang3', 'password', 'Yibo', 'Zhang', '');
Insert into PersonPhone values ('BuxiaoChu1', '1234567890');
Insert into PersonPhone values ('XingyuXian2', '0987654321');
Insert into PersonPhone values ('YiboZhang3', '1357924680');
Insert into Act values ('BuxiaoChu1', '4');
Insert into Act values ('XingyuXian2', '3');
Insert into Act values ('YiboZhang3', '2');

Insert into Item values ('1001', 'A yellow sofa', '', 'yellow', TRUE, '1', 'leather');
Insert into DonatedBy values ('BuxiaoChu1', '1001', '2024-11-01');
Insert into Piece values('10001', 'cushion', '30', '30', '5');
Insert into Piece values('10002', 'sofa body', '35', '35', '60');
Insert into Category values('Furniture', 'Sofa', 'A place to sit');
Insert into ItemCategory values('Furniture', 'Sofa', '1001');
Insert into `Of` values('10001', '1001');
Insert into `Of` values('10002', '1001');
Insert into `Location` values('5', '0', '');
Insert into PieceIn values( '5', '0', '10001', '');
Insert into PieceIn values( '5', '0', '10002', '');

-- C.b.
Insert into Item values ('1002', 'A dining table set', '', 'brown', TRUE, '3', 'wood');
Insert into DonatedBy values ('BuxiaoChu1', '1002', '2024-10-01');
Insert into Piece values('10003', 'chair_1', '20', '20', '50');
Insert into Piece values('10004', 'chair_2', '30', '30', '50');
Insert into Piece values('10005', 'table', '100', '100', '120');
Insert into Category values('Furniture', 'Tables', 'A place to have meals');
Insert into ItemCategory values('Furniture', 'Tables', '1002');
Insert into `Of` values('10003', '1002');
Insert into `Of` values('10004', '1002');
Insert into `Of` values('10005', '1002');
Insert into `Location` values('4', '1', 'The first shelf in Room 4');
Insert into PieceIn values('4', '1', '10003', '');
Insert into PieceIn values('4', '1', '10004', '');
Insert into PieceIn values('4', '1', '10005', '');

Insert into `Order` values('12345', '2024-10-02', 'A dining table');
Insert into ItemIn values('1002', '12345', TRUE);
Insert into `For` values('12345', 'XingyuXian2');
Insert into Supervised values('12345', 'YiboZhang3');
Insert into Delivered values('12345', 'YiboZhang3', 'delivered', '2024-10-03');

SELECT 
    p.pieceNum AS PieceNum,
    i.itemID AS ItemID,
    i.idescription AS ItemDescription,
    p.pDescription AS PieceDscription,
    c.mainCategory AS MainCategory,
    c.subCategory AS SubCategory,
    l.roomNum AS RoomNum,
    l.shelfNum AS Shelf,
    l.shelfDescription AS LocationDescription
FROM 
    Item i
JOIN 
    ItemIn ii ON i.itemID = ii.itemID
JOIN 
    `Order` o ON ii.orderID = o.orderID
JOIN 
    `Of` ofTable ON i.itemID = ofTable.itemID
JOIN 
    Piece p ON ofTable.pieceNum = p.pieceNum
JOIN 
    PieceIn pi ON p.pieceNum = pi.pieceNum
JOIN 
    Location l ON pi.roomNum= l.roomNum AND pi.shelfNum = l.shelfNum
JOIN 
    ItemCategory ic ON i.itemID = ic.itemID
JOIN 
    Category c ON ic.mainCategory = c.mainCategory AND ic.subCategory = c.subCategory
WHERE 
    o.orderID = '12345'
ORDER BY 
    p.pieceNum;

-- more data: cooking set
Insert into Item values ('1003', 'A kitchen cooking set', '', 'silver', TRUE, '3', 'steel');
Insert into DonatedBy values ('BuxiaoChu1', '1003', '2024-11-01');
Insert into Piece values('10006', 'knives', '5', '5', '1');
Insert into Piece values('10007', 'forks', '5', '5', '1');
Insert into Piece values('10008', 'spoons', '5', '5', '1');
Insert into Category values('Furniture', 'Utensils', 'Cooking tools');
Insert into ItemCategory values('Furniture', 'Utensils', '1003');
Insert into `Of` values('10006', '1003');
Insert into `Of` values('10007', '1003');
Insert into `Of` values('10008', '1003');
Insert into `Location` values('5', '2', 'The second shelf in Room 5');
Insert into PieceIn values('5', '2', '10006', '');
Insert into PieceIn values('5', '2', '10007', '');
Insert into PieceIn values('5', '2', '10008', '');

Insert into `Order` values('11111', '2024-11-02', 'A cooking set');
Insert into ItemIn values('1003', '11111', TRUE);
Insert into `For` values('11111', 'XingyuXian2');
Insert into Supervised values('11111', 'YiboZhang3');
Insert into Delivered values('11111', 'YiboZhang3', 'delivered', '2024-11-03');