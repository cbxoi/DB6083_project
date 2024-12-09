## Database Project Part 3:

##### Buxiao Chu, bc3730

##### Xingyu Xian xx2360

##### Yibo Zhang, yz10589



**Languages:** Python, SQL, HTML

**framework:** Flask, Jinja2

**feature chosen:** 5, 6, 7, 8, 12



## Schema

Our schemas are based on Project Schema-v2

Due to the implement of Feature 12 and other features, we change the schemas as follows:


#### Item
Item(**ItemID**, quantityNum, iDescription, photo, color, isNew, hasPieces, material, mainCategory, subCategory)

Item(mainCategory, subCategory) REFERENCES Category(mainCategory, subCategory)

<br>

Added `quantityNum` to it but not as a primary key.

When the same item added to the database, we just increase its quantity.

When donating, the staff will check if two items are the same so that they should have the same itemID.

Here is an assumption: We just suppose that the same kind of pieces are stored in the same location. If they have different locations, we will face a complex dispatch problem when shopping and delivering.

No AUTO_INCREMENT on `ItemID`

<br>


#### DonatedBy

DonatedBy(**ItemID**, quantityNum, **userName**, **donateDate**)  

DonatedBy(ItemID) REFERENCES Item(ItemID)

DonatedBy(userName) REFERENCES Person(userName)

<br>

Added `quantityNum`to it but not as a primary key. Set donateDate as a primary key.

Because of the possible duplicated items, the same person might donate the same item in different date.

We just add this record into Donatedby. It has no effect on shopping.

Changed primary key to (**ItemID**, quantityNum, **userName**, **donateDate**)

<br>

#### ItemIn

ItemIn(**ItemID**, quantityNum, **orderID**, found, status, holdingRoomNum, holdingShelfNum)  

ItemIn(ItemID) REFERENCES Item(ItemID)

ItemIn(orderID) REFERENCES Ordered(orderID)  

ItemIn(holdingRoomNum, holdingShelfNum) REFERENCES Location(roomNum, shelfNum)

<br>

Added `quantityNum` to it but not as a primary key.

Added `holdingRoomNum` for holding location for item

Added `holdingShelfNum` for holding location for item

Added `status` to view item status (for holding location feature)

<br>


#### Delivered
status ENUM('Pending', 'In Transit', 'Delivered', 'Cancelled') NOT NULL,
date DATE NOT NULL

<br>

Added `status` 


<br>


### Pages:

**Index, login, register** - the same as the demo

**person** -  the home page, several functional links

**find_item** - show the information of the item's pieces 

**find_order** - show the information of the order's items

**donor_got** - input of the information of a item from the user

**item_added** - input of the information of relevant pieces (if exists) from the user

**prepare_order** - input of the information of holding location of an order

**user_orders** - show all the orders the current user 



## Queries

**Feature 1:**

```sql
# login
SELECT * FROM Person WHERE userName = %s and password = %s

# register
# check if the user exists
SELECT * FROM Person WHERE userName = %s
# insert the user into database
INSERT INTO Person VALUES(%s, %s, %s, %s, %s)
insert into PersonPhone values(%s, %s)
insert into act values(%s, %s)
```



**Feature 2:**

```sql
# find item
select * from piece where itemID = %s
```



**Feature 3:**

```sql
# find order
# select items from the order
select * from ItemIn where orderID = %s
# count the item in the order
select count(*) as count from ItemIn where orderID = %s
# select the pieces of the items
select * from piece where itemID = %s
```



**Feature 4:**

```sql
# accept donation
# check if the user is a staff
select * from act where username = %s
# check if the user entered is a donor
select * from act where username = %s

# add item
# check if the item exists
select * from item where itemID = %s
# if it exists, update the quantity of this item
update item set quantityNum = quantityNum + %s where itemID = %s
insert into donatedby values(%s, %s, %s, %s)
# if it doesn`t exist, insert it into database
insert into item values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
insert into donatedby values(%s, %s, %s, %s)

# add pieces
# if the item has pieces, insert them into database
insert into piece values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
# show the pieces that have been added
select * from piece where itemID = %s
```

**Feature 7:**
```sql
# Search orders by username
SELECT o.orderID, o.orderDate, o.orderNotes
FROM Ordered o
JOIN Person p ON o.client = p.userName
WHERE p.userName = %s

# Search orders by order ID
SELECT i.ItemID, i.quantityNum, i.status, l.roomNum, l.shelfNum, l.shelfDescription
FROM ItemIn i
LEFT JOIN Location l ON i.holdingRoomNum = l.roomNum AND i.holdingShelfNum = l.shelfNum
WHERE i.orderID = %s

# Ensure location exists in the Location table
SELECT COUNT(*) AS count FROM Location WHERE roomNum = %s AND shelfNum = %s

# Insert new location if it does not exist
INSERT INTO Location (roomNum, shelfNum, shelf, shelfDescription)
VALUES (%s, %s, %s, %s)

# Update item location and status
#if change status to holding
UPDATE ItemIn
SET status = 'Holding', holdingRoomNum = %s, holdingShelfNum = %s
WHERE orderID = %s AND status = 'Available'

#if change status to avaliable
UPDATE ItemIn
SET status = 'Available', holdingRoomNum = %s, holdingShelfNum = %s
WHERE orderID = %s

# fetch updated data to dislay on website
SELECT i.ItemID, i.quantityNum, i.status, l.roomNum, l.shelfNum, l.shelfDescription
FROM ItemIn i
LEFT JOIN Location l ON i.holdingRoomNum = l.roomNum AND i.holdingShelfNum = l.shelfNum
WHERE i.orderID = %s
```

**Feature 8:**
```sql
# Fetch all orders associated with the current user
SELECT o.orderID, o.orderDate, o.orderNotes, o.supervisor, o.client, i.ItemID, i.quantityNum, i.status
FROM Ordered o
LEFT JOIN ItemIn i ON o.orderID = i.orderID
WHERE o.client = %s OR EXISTS (
        SELECT 1 FROM Delivered d WHERE d.orderID = o.orderID AND d.userName = %s
        )
```



#### Difficulties

1. We suppose that the same items are stored in the same location. It's known that in the real Logistics and transportation system, here`s a dispatch problem. The system needs to choose a appropriate warehouse and assign a delivery for clients. But we cant handle this.



#### Division of Labor

**Buxiao Chu**

frame construction

provide data

feature 1,2,3,4 (12) coding, testing

**Xingyu Xian**

schemas revision

edit data

feature 7,8 coding, testing

**Yibo Zhang**

provide data

feature 5,6 coding, testing