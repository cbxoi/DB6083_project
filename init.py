from datetime import datetime

#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors


#for uploading photo:
from app import app
#from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


###Initialize the app from Flask
app = Flask(__name__)
app.secret_key = "secret key"

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='root',
                       db='welcomehome',
                       charset='utf8mb4',
                       cursorclass=pymysql.cursors.DictCursor)


def allowed_image(filename):

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_IMAGE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_image_filesize(filesize):

    if int(filesize) <= app.config["MAX_IMAGE_FILESIZE"]:
        return True
    else:
        return False


#Define a route to hello function
@app.route('/')
def hello():
    return render_template('index.html')

#Define route for login
@app.route('/login')
def login():
    return render_template('login.html')

#Define route for register
@app.route('/register')
def register():
    return render_template('register.html')

#Authenticates the login
@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE userName = %s and password = %s'
    cursor.execute(query, (username, password))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if(data):
        #creates a session for the the user
        #session is a built in
        session['username'] = username
        return redirect(url_for('person'))
    else:
        #returns an error message to the html page
        error = 'Invalid login or username'
        return render_template('login.html', error=error)

#Authenticates the register
@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    #grabs information from the forms
    username = request.form['username']
    password = request.form['password']
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']
    phone = request.form['phone']
    role = request.form['role']

    if(not username or not password or not email or not phone):
      error = "Information needed!"
      return render_template('register.html', error = error)
    if(not role):
      error = "A role needed to be selected!"
      return render_template('register.html', error = error)

    #cursor used to send queries
    cursor = conn.cursor()
    #executes query
    query = 'SELECT * FROM Person WHERE userName = %s'
    cursor.execute(query, (username))
    #stores the results in a variable
    data = cursor.fetchone()
    #use fetchall() if you are expecting more than 1 data row
    error = None
    if(data):
        #If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template('register.html', error = error)
    else:
        #Insert the user into the database
        ins = 'INSERT INTO Person VALUES(%s, %s, %s, %s, %s)'
        cursor.execute(ins, (username, password, fname, lname, email))
        ins = 'insert into PersonPhone values(%s, %s)'
        cursor.execute(ins, (username, phone))
        ins = 'insert into act values(%s, %s)'
        cursor.execute(ins, (username, role))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/person')
def person():
    #set the session
    user = session['username']
    return render_template('person.html', username=user)

#feature 2
#this action is in person.html
@app.route('/action_find_item', methods=['POST'])
def find_item():
    itemID = request.form['itemID']
    cursor = conn.cursor()
    # a query to find the pieces of the item and their locations
    query = 'select * from piece where itemID = %s'
    cursor.execute(query, itemID)
    pieces = cursor.fetchall()
    cursor.close()
    return render_template('find_item.html', itemID=itemID, pieces=pieces)

#feature 3
#this action is in person.html
@app.route('/action_find_order', methods=['POST'])
def find_order():
    orderID = request.form['orderID']
    cursor = conn.cursor()
    # a query to find items in the order
    query = 'select * from ItemIn where orderID = %s'
    cursor.execute(query, orderID)
    items = cursor.fetchall()

    # a query to count the number of items in the order
    query = 'select count(*) as count from ItemIn where orderID = %s'
    cursor.execute(query, orderID)
    count = cursor.fetchone()
    
    # Add information about the pieces of the items to the items tuples
    items = list(items)
    for item in items:
        # a query to find the pieces of the item and their locations
        query = 'select * from piece where itemID = %s'
        cursor.execute(query, item['ItemID'])
        item['pieces'] = cursor.fetchall()
    items = tuple(items)
    cursor.close()
    return render_template('find_order.html', orderID=orderID, quantity=count['count'], items=items)

#feature 4
#this action is in person.html
@app.route('/action_accept_donation', methods=['POST'])
def accept_donation():
    username = session['username']
    donorname = request.form['donorname']
    cursor = conn.cursor()
    # a query to find the user
    query = 'select * from act where username = %s'
    cursor.execute(query, username)
    user = cursor.fetchone()
    if user['roleID'] != 'staff':
        cursor.close()
        error = 'This user is not a staff'
        return render_template('person.html', username=username ,error=error)
    
    # a query to find the donor
    query = 'select * from act where username = %s'
    cursor.execute(query, donorname)
    donor = cursor.fetchone()
    cursor.close()

    # check if the donor exists and is a donor
    if donor['roleID'] != 'donor':
        error = 'This user is not a donor'
        return render_template('person.html', username=username ,error=error)
    if not donor:
        error = 'Cannot find this donor'
        return render_template('person.html', username=username ,error=error)
    
    #set session
    session['donor'] = donorname
    return render_template('donor_got.html', username=donor)

#accept_donation.html is not used now
# @app.route('/get_donor', methods=['POST'])
# def get_donor():
#     donor = request.form['username']
#     cursor = conn.cursor()
#     # a query to find the donor
#     query = 'select * from person where username = %s'
#     cursor.execute(query, donor)
#     user = cursor.fetchone()
#     cursor.close()
#     if user:
#         session['donor'] = donor
#         return render_template('donor_got.html')
#     else:
#         error = 'This user is not a donor!'
#         return render_template('accept_donation.html', error=error)

#feature 4
#this action is in donor_got.html
#add item and render pieces adding page if the item has pieces
@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    donor = session['donor']
    itemID = request.form['ItemID']
    quantity = request.form['quantity']
    iDesc = request.form['iDesc']
    color = request.form['color']
    isNew = request.form['isNew']
    hasPieces = request.form['hasPieces']
    material = request.form['material']
    mainCategory = request.form['mainCategory']
    subCategory = request.form['subCategory']

    cursor = conn.cursor()
    # a query to find if the item exists
    query = 'select * from item where itemID = %s'
    cursor.execute(query, itemID)
    item = cursor.fetchone()

    # if the item exists in the database
    if item:
        # increase the quantity of the item by quantity
        upd = 'update item set quantityNum = quantityNum + %s where itemID = %s'
        cursor.execute(upd, (quantity, itemID))
        # insert the donation into the database
        ins = 'insert into donatedby values(%s, %s, %s, %s)'
        cursor.execute(ins, (itemID, donor, quantity, datetime.now()))
        conn.commit()
        cursor.close()
        session.pop('donor')
        return render_template('person.html', success='Item added successfully!')
    else:
        # insert the item into the database
        ins = 'insert into item values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(ins, (itemID, quantity, iDesc, color, 0, isNew, hasPieces, material, mainCategory, subCategory))
        # insert the donation into the database
        ins = 'insert into donatedby values(%s, %s, %s, %s)'
        cursor.execute(ins, (itemID, donor, quantity, datetime.now()))
        conn.commit()
        cursor.close()
        # if the item has pieces, set the session and enter 'add_pieces' page
        if hasPieces == "1":
            session['itemID'] = itemID
            return render_template('item_added.html', itemID=itemID)
        # remove the session
        session.pop('donor')
        return render_template('person.html', success='Item added successfully!')

#feature 4
#this action is in item_added.html
@app.route('/add_pieces', methods=['GET','POST'])
def add_pieces():
    donor = session['donor']
    itemID = session['itemID']

    pieceNum = request.form['pieceNum']
    pDesc = request.form['pDesc']
    length = request.form['length']
    width = request.form['width']
    height = request.form['height']
    roomNum = request.form['roomNum']
    shelfNum = request.form['shelfNum']
    pNotes = request.form['pNotes']

    # check if all fields are filled
    if not pieceNum or not pDesc or not length or not width or not height or not roomNum or not shelfNum:
        flash('Please fill out all fields')
        return render_template('item_added.html')

    cursor = conn.cursor()
    # Insert the piece into the database
    ins = 'insert into piece values(%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    cursor.execute(ins, (session['itemID'], pieceNum, pDesc, length, width, height, roomNum, shelfNum, pNotes))
    conn.commit()

    # a query to find the pieces of the item and their locations
    query = 'select * from piece where itemID = %s'
    cursor.execute(query, itemID)
    item = cursor.fetchall()
    cursor.close()
    flash('Piece added successfully')
    return render_template('item_added.html', itemID=itemID, item=item)

#feature 4
#this action is in item_added.html
#end adding pieces and return to home page
@app.route('/end_adding_pieces', methods=['GET'])
def end_adding_pieces():
    #remove the session
    session.pop('itemID')
    session.pop('donor')
    return render_template('person.html', success='Item added successfully!')


#------------------------------------------------------------------------------


@app.route('/post', methods=['GET', 'POST'])
def post():
    username = session['username']
    cursor = conn.cursor()
    blog = request.form['blog']
    query = 'INSERT INTO blog (blog_post, username) VALUES(%s, %s)'
    cursor.execute(query, (blog, username))
    conn.commit()
    cursor.close()
    return redirect(url_for('home'))

@app.route('/select_blogger')
def select_blogger():
    #check that user is logged in
    #username = session['username']
    #should throw exception if username not found
    
    cursor = conn.cursor();
    query = 'SELECT DISTINCT username FROM blog'
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return render_template('select_blogger.html', user_list=data)

@app.route('/show_posts', methods=["GET", "POST"])
def show_posts():
    poster = request.args['poster']
    cursor = conn.cursor()
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, poster)
    data = cursor.fetchall()
    cursor.close()
    return render_template('show_posts.html', poster_name=poster, posts=data)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/upload_form', methods=['GET'])
def upload_form():
    return render_template('upload.html')

@app.route('/upload_file', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
			flash('File successfully uploaded')
			return redirect('/')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

#------------------------------------------------------------------------------

@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')


#------------------------------------------------------------------------------
#feature 7
@app.route('/prepare_order', methods=['GET', 'POST'])
def prepare_order():
    cursor = conn.cursor()

    if request.method == 'POST':
        # Collect form data
        client_username = request.form.get('username')
        order_id = request.form.get('orderID')
        room_number = request.form.get('roomNumber')
        shelf_number = request.form.get('shelfNumber')

        # **Search Operation**
        if client_username or (order_id and not room_number):
            if client_username:
                # Search orders by username
                query = '''
                    SELECT o.orderID, o.orderDate, o.orderNotes
                    FROM Ordered o
                    JOIN Person p ON o.client = p.userName
                    WHERE p.userName = %s
                '''
                cursor.execute(query, (client_username,))
                orders = cursor.fetchall()

                if not orders:
                    return render_template('prepare_order.html', error=f"No orders found for client {client_username}.")
                
                return render_template('prepare_order.html', orders=orders)

            elif order_id:
                # Search orders by order ID
                query = 'SELECT * FROM Ordered WHERE orderID = %s'
                cursor.execute(query, (order_id,))
                order = cursor.fetchone()

                if not order:
                    return render_template('prepare_order.html', error=f"Order ID {order_id} does not exist.")
                
                item_query = '''
                    SELECT i.ItemID, i.quantityNum, i.status, l.roomNum, l.shelfNum, l.shelfDescription
                    FROM ItemIn i
                    LEFT JOIN Location l ON i.holdingRoomNum = l.roomNum AND i.holdingShelfNum = l.shelfNum
                    WHERE i.orderID = %s
                '''
                cursor.execute(item_query, (order_id,))
                items = cursor.fetchall()

                return render_template('prepare_order.html', order=order, items=items)

        # **Update Location Operation**
        if order_id and room_number:
            try:
                # Ensure location exists in the Location table
                location_check_query = '''
                    SELECT COUNT(*) AS count FROM Location WHERE roomNum = %s AND shelfNum = %s
                '''
                cursor.execute(location_check_query, (room_number, shelf_number))
                location_exists = cursor.fetchone()['count']

                if not location_exists:
                    # Insert new location if it doesn't exist
                    insert_location_query = '''
                        INSERT INTO Location (roomNum, shelfNum, shelf, shelfDescription)
                        VALUES (%s, %s, %s, %s)
                    '''
                    cursor.execute(insert_location_query, (room_number, shelf_number, 'Holding', 'Holding area for ready items'))
                    conn.commit()

                # Update item location and status
                if int(room_number) == 99:
                    update_query = '''
                        UPDATE ItemIn
                        SET status = 'Holding', holdingRoomNum = %s, holdingShelfNum = %s
                        WHERE orderID = %s AND status = 'Available'
                    '''
                else:
                    update_query = '''
                        UPDATE ItemIn
                        SET status = 'Available', holdingRoomNum = %s, holdingShelfNum = %s
                        WHERE orderID = %s
                    '''
                cursor.execute(update_query, (room_number, shelf_number, order_id))
                conn.commit()

                # Fetch updated data
                item_query = '''
                    SELECT i.ItemID, i.quantityNum, i.status, l.roomNum, l.shelfNum, l.shelfDescription
                    FROM ItemIn i
                    LEFT JOIN Location l ON i.holdingRoomNum = l.roomNum AND i.holdingShelfNum = l.shelfNum
                    WHERE i.orderID = %s
                '''
                cursor.execute(item_query, (order_id,))
                items = cursor.fetchall()

                query = 'SELECT * FROM Ordered WHERE orderID = %s'
                cursor.execute(query, (order_id,))
                order = cursor.fetchone()

                return render_template('prepare_order.html', success=f"Order {order_id} updated with Room {room_number} and Shelf {shelf_number}.", order=order, items=items)

            except Exception as e:
                conn.rollback()
                print(f"Error updating order: {e}")
                return render_template('prepare_order.html', error="An error occurred while updating the order. Please try again.")

        # If neither a search nor update, return an error
        return render_template('prepare_order.html', error="Room number and shelf number are required to update location.")

    # **Handle GET Requests**
    # If GET and `orderID` is provided in the query string, display order details
    order_id = request.args.get('orderID')
    if order_id:
        query = 'SELECT * FROM Ordered WHERE orderID = %s'
        cursor.execute(query, (order_id,))
        order = cursor.fetchone()

        if order:
            item_query = '''
                SELECT i.ItemID, i.quantityNum, i.status, l.roomNum, l.shelfNum, l.shelfDescription
                FROM ItemIn i
                LEFT JOIN Location l ON i.holdingRoomNum = l.roomNum AND i.holdingShelfNum = l.shelfNum
                WHERE i.orderID = %s
            '''
            cursor.execute(item_query, (order_id,))
            items = cursor.fetchall()

            return render_template('prepare_order.html', order=order, items=items)

    return render_template('prepare_order.html')


#------------------------------------------------------------------------------
#feature 8
@app.route('/user_orders', methods=['GET'])
def user_orders():
    # Get the current logged-in user
    username = session.get('username')
    if not username:
        return redirect(url_for('login'))

    # Fetch all orders associated with the current user
    cursor = conn.cursor()
    query = '''
        SELECT o.orderID, o.orderDate, o.orderNotes, o.supervisor, o.client
        FROM Ordered o
        LEFT JOIN Delivered d ON o.orderID = d.orderID
        WHERE o.client = %s OR d.userName = %s
    '''
    cursor.execute(query, (username, username))
    orders = cursor.fetchall()
    cursor.close()

    # Render the results
    return render_template('user_orders.html', orders=orders, username=username)





print(app.url_map)

app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)










