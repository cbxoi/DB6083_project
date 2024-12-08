## Database Project Part 3:

##### Buxiao Chu, bc3730

##### Xingyu Xian xx2360

##### Yibo Zhang, yz10589



**Languages:** Python and html

**framework:** flask

**feature chosen:** 5, 6, 7, 8, 12



#### schema

Our schemas are based on Project Schema-v2

Due to the implement of Feature 12, we change the schemas as follows:





#### Pages:

**Index, login, register** - the same as the demo

**person** -  the home page, several functional links

**find_item** - show the information of the item's pieces 

**find_order** - show the information of the order's items

**donor_got** - input of the information of a item from the user

**item_added** - input of the information of relevant pieces (if exists) from the user



#### Queries

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
# if it exists, update the quantity of the item
update item set quantityNum = quantityNum + %s where itemID = %s
# if it doesn't exist, insert it into database
insert into item values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
insert into donatedby values(%s, %s, %s, %s)

# add pieces
# if the item has pieces, insert them into database
insert into piece values(%s, %s, %s, %s, %s, %s, %s, %s, %s)
# show the pieces that have been added
select * from piece where itemID = %s
```





#### Division of Labor

**Buxiao Chu**

frame construction

provide data

feature 1,2,3,4 (12) coding, testing

**Xingyu Xian**

schemas revision

feature 7,8 coding

**Yibo Zhang**

provide data

feature 5,6 coding