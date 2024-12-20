from datetime import datetime

# Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors


# for uploading photo:
from app import app

# from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "gif"])


###Initialize the app from Flask
app = Flask(__name__)
app.secret_key = "secret key"

# Configure MySQL
conn = pymysql.connect(
    host="localhost",
    port=3306,
    user="root",
    password="root",
    db="welcomehome",
    charset="utf8mb4",
    cursorclass=pymysql.cursors.DictCursor,
)


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


# Define a route to hello function
@app.route("/")
def hello():
    return render_template("index.html")


# Define route for login
@app.route("/login")
def login():
    return render_template("login.html")


# Define route for register
@app.route("/register")
def register():
    return render_template("register.html")


# Authenticates the login
@app.route("/loginAuth", methods=["GET", "POST"])
def loginAuth():
    # grabs information from the forms
    username = request.form["username"]
    password = request.form["password"]

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = "SELECT * FROM Person WHERE userName = %s and password = %s"
    cursor.execute(query, (username, password))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    cursor.close()
    error = None
    if data:
        # creates a session for the the user
        # session is a built in
        session["username"] = username
        return redirect(url_for("person"))
    else:
        # returns an error message to the html page
        error = "Invalid login or username"
        return render_template("login.html", error=error)


# Authenticates the register
@app.route("/registerAuth", methods=["GET", "POST"])
def registerAuth():
    # grabs information from the forms
    username = request.form["username"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    email = request.form["email"]
    phone = request.form["phone"]
    role = request.form["role"]

    if not username or not password or not email or not phone:
        error = "Information needed!"
        return render_template("register.html", error=error)
    if not role:
        error = "A role needed to be selected!"
        return render_template("register.html", error=error)

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = "SELECT * FROM Person WHERE userName = %s"
    cursor.execute(query, (username))
    # stores the results in a variable
    data = cursor.fetchone()
    # use fetchall() if you are expecting more than 1 data row
    error = None
    if data:
        # If the previous query returns data, then user exists
        error = "This user already exists"
        return render_template("register.html", error=error)
    else:
        # Insert the user into the database
        ins = "INSERT INTO Person VALUES(%s, %s, %s, %s, %s)"
        cursor.execute(ins, (username, password, fname, lname, email))
        ins = "insert into PersonPhone values(%s, %s)"
        cursor.execute(ins, (username, phone))
        ins = "insert into act values(%s, %s)"
        cursor.execute(ins, (username, role))
        conn.commit()
        cursor.close()
        return render_template("index.html")


@app.route("/person")
def person():
    # set the session
    user = session["username"]
    return render_template("person.html", username=user)


# feature 2
# this action is in person.html
@app.route("/action_find_item", methods=["POST"])
def find_item():
    itemID = request.form["itemID"]
    cursor = conn.cursor()
    # a query to find the pieces of the item and their locations
    query = "select * from piece where itemID = %s"
    cursor.execute(query, itemID)
    pieces = cursor.fetchall()
    cursor.close()
    return render_template("find_item.html", itemID=itemID, pieces=pieces)


# feature 3
# this action is in person.html
@app.route("/action_find_order", methods=["POST"])
def find_order():
    orderID = request.form["orderID"]
    cursor = conn.cursor()
    # a query to find items in the order
    query = "select * from ItemIn where orderID = %s"
    cursor.execute(query, orderID)
    items = cursor.fetchall()

    # a query to count the number of items in the order
    query = "select count(*) as count from ItemIn where orderID = %s"
    cursor.execute(query, orderID)
    count = cursor.fetchone()

    # Add information about the pieces of the items to the items tuples
    items = list(items)
    for item in items:
        # a query to find the pieces of the item and their locations
        query = "select * from piece where itemID = %s"
        cursor.execute(query, item["ItemID"])
        item["pieces"] = cursor.fetchall()
    items = tuple(items)
    cursor.close()
    return render_template(
        "find_order.html", orderID=orderID, quantity=count["count"], items=items
    )


# feature 4
# this action is in person.html
@app.route("/action_accept_donation", methods=["POST"])
def accept_donation():
    username = session["username"]
    donorname = request.form["donorname"]
    cursor = conn.cursor()
    # a query to find the user
    query = "select * from act where username = %s"
    cursor.execute(query, username)
    user = cursor.fetchone()
    if user["roleID"] != "staff":
        cursor.close()
        error = "This user is not a staff"
        return render_template("person.html", username=username, error=error)

    # a query to find the donor
    query = "select * from act where username = %s"
    cursor.execute(query, donorname)
    donor = cursor.fetchone()
    cursor.close()

    # check if the donor exists and is a donor
    if donor["roleID"] != "donor":
        error = "This user is not a donor"
        return render_template("person.html", username=username, error=error)
    if not donor:
        error = "Cannot find this donor"
        return render_template("person.html", username=username, error=error)

    # set session
    session["donor"] = donorname
    return render_template("donor_got.html", username=donor)


# accept_donation.html is not used now
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


# feature 4
# this action is in donor_got.html
# add item and render pieces adding page if the item has pieces
@app.route("/add_item", methods=["GET", "POST"])
def add_item():
    donor = session["donor"]
    itemID = request.form["ItemID"]
    quantity = request.form["quantity"]
    iDesc = request.form["iDesc"]
    color = request.form["color"]
    isNew = request.form["isNew"]
    hasPieces = request.form["hasPieces"]
    material = request.form["material"]
    mainCategory = request.form["mainCategory"]
    subCategory = request.form["subCategory"]

    cursor = conn.cursor()
    # a query to find if the item exists
    query = "select * from item where itemID = %s"
    cursor.execute(query, itemID)
    item = cursor.fetchone()

    # if the item exists in the database
    if item:
        # increase the quantity of the item by quantity
        upd = "update item set quantityNum = quantityNum + %s where itemID = %s"
        cursor.execute(upd, (quantity, itemID))
        # insert the donation into the database
        ins = "insert into donatedby values(%s, %s, %s, %s)"
        cursor.execute(ins, (itemID, donor, quantity, datetime.now()))
        conn.commit()
        cursor.close()
        session.pop("donor")
        return render_template("person.html", success="Item added successfully!")
    else:
        # insert the item into the database
        ins = "insert into item values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(
            ins,
            (
                itemID,
                quantity,
                iDesc,
                color,
                0,
                isNew,
                hasPieces,
                material,
                mainCategory,
                subCategory,
            ),
        )
        # insert the donation into the database
        ins = "insert into donatedby values(%s, %s, %s, %s)"
        cursor.execute(ins, (itemID, donor, quantity, datetime.now()))
        conn.commit()
        cursor.close()
        # if the item has pieces, set the session as True
        if hasPieces == "1":
            session["itemID"] = itemID
            return render_template("item_added.html", itemID=itemID)
        # remove the session
        session.pop("donor")
        return render_template("person.html", success="Item added successfully!")


# feature 4
# this action is in item_added.html
@app.route("/add_pieces", methods=["GET", "POST"])
def add_pieces():
    donor = session["donor"]
    itemID = session["itemID"]

    pieceNum = request.form["pieceNum"]
    pDesc = request.form["pDesc"]
    length = request.form["length"]
    width = request.form["width"]
    height = request.form["height"]
    roomNum = request.form["roomNum"]
    shelfNum = request.form["shelfNum"]
    pNotes = request.form["pNotes"]

    # check if all fields are filled
    if (
        not pieceNum
        or not pDesc
        or not length
        or not width
        or not height
        or not roomNum
        or not shelfNum
    ):
        flash("Please fill out all fields")
        return render_template("item_added.html")

    cursor = conn.cursor()
    # Insert the piece into the database
    ins = "insert into piece values(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(
        ins,
        (
            session["itemID"],
            pieceNum,
            pDesc,
            length,
            width,
            height,
            roomNum,
            shelfNum,
            pNotes,
        ),
    )
    conn.commit()

    # a query to find the pieces of the item and their locations
    query = "select * from piece where itemID = %s"
    cursor.execute(query, itemID)
    item = cursor.fetchall()
    cursor.close()
    flash("Piece added successfully")
    return render_template("item_added.html", itemID=itemID, item=item)


# feature 4
# this action is in item_added.html
# end adding pieces and return to home page
@app.route("/end_adding_pieces", methods=["GET"])
def end_adding_pieces():
    if session['pieceNum'] == 0:
        flash('Please add at least one piece')
        return render_template('item_added.html', itemID=session['itemID'])
    #remove the session
    session.pop('hasPieces')
    session.pop('itemID')
    session.pop('pieceNum')
    session.pop('donor')
    return render_template('person.html', success='Item added successfully!')


# ------------------------------------------------------------------------------


@app.route("/post", methods=["GET", "POST"])
def post():
    username = session["username"]
    cursor = conn.cursor()
    blog = request.form["blog"]
    query = "INSERT INTO blog (blog_post, username) VALUES(%s, %s)"
    cursor.execute(query, (blog, username))
    conn.commit()
    cursor.close()
    return redirect(url_for("home"))


# @app.route("/select_blogger")
# def select_blogger():
#     # check that user is logged in
#     # username = session['username']
#     # should throw exception if username not found

#     cursor = conn.cursor()
#     query = "SELECT DISTINCT username FROM blog"
#     cursor.execute(query)
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template("select_blogger.html", user_list=data)


# @app.route("/show_posts", methods=["GET", "POST"])
# def show_posts():
#     poster = request.args["poster"]
#     cursor = conn.cursor()
#     query = "SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC"
#     cursor.execute(query, poster)
#     data = cursor.fetchall()
#     cursor.close()
#     return render_template("show_posts.html", poster_name=poster, posts=data)


# def allowed_file(filename):
#     return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# @app.route("/upload_form", methods=["GET"])
# def upload_form():
#     return render_template("upload.html")


# @app.route("/upload_file", methods=["POST"])
# def upload_file():
#     if request.method == "POST":
#         # check if the post request has the file part
#         if "file" not in request.files:
#             flash("No file part")
#             return redirect(request.url)
#         file = request.files["file"]
#         if file.filename == "":
#             flash("No file selected for uploading")
#             return redirect(request.url)
#         if file and allowed_file(file.filename):
#             filename = secure_filename(file.filename)
#             file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
#             flash("File successfully uploaded")
#             return redirect("/")
#         else:
#             flash("Allowed file types are txt, pdf, png, jpg, jpeg, gif")
#             return redirect(request.url)


# ------------------------------------------------------------------------------


@app.route("/logout")
def logout():
    session.pop("username")
    return redirect("/")


# ------------------------------------------------------------------------------
# feature 5


def is_staff(username):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM Act WHERE userName = %s AND roleID = 'staff'", (username,)
        )
        return cursor.fetchone() is not None


def is_valid_client(username):
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT 1 FROM Act WHERE userName = %s AND roleID = 'client'", (username,)
        )
        return cursor.fetchone() is not None


# Start an Order
@app.route("/start_order", methods=["GET", "POST"])
def start_order():
    error = None
    success = None
    if "username" not in session or not is_staff(session["username"]):
        error = "You must be logged in as a staff member to start an order."
        print("Error: Not logged in or not a staff member")
        return render_template("person.html", error=error)

    if request.method == "POST":
        client_username = request.form["client_username"]
        print("Client username submitted:", client_username)

        if not is_valid_client(client_username):
            error = "Invalid client username."
            print("Error: Invalid client username")
            return render_template("start_order.html", error=error)

        with conn.cursor() as cursor:
            try:
                cursor.execute(
                    "INSERT INTO Ordered (orderDate, orderNotes, supervisor, client) VALUES (CURDATE(), %s, %s, %s)",
                    ("New Order", session["username"], client_username),
                )
                conn.commit()
                print("Order successfully inserted into database")

                cursor.execute("SELECT LAST_INSERT_ID() AS orderID")
                order_id_result = cursor.fetchone()
                if not order_id_result or "orderID" not in order_id_result:
                    print("Error: Failed to fetch orderID after insert")
                    error = "Failed to fetch order ID. Please try again."
                    return render_template("start_order.html", error=error)

                order_id = order_id_result["orderID"]
                session["current_order"] = order_id
                success = f"Order #{order_id} has been created."
                print("Redirecting to add_to_order with success message")
                return redirect(url_for("add_to_order", success=success))
            except Exception as e:
                error = "Failed to create the order. Please try again."
                print("Database error:", e)
                return render_template("start_order.html", error=error)

    return render_template("start_order.html")


# ------------------------------------------------------------------------------
# Feature 6: Add to Order
@app.route("/add_to_order", methods=["GET", "POST"])
def add_to_order():
    error = None
    success = None
    items = []

    if "current_order" not in session:
        error = "No active order. Start an order first."
        return redirect(url_for("start_order"))
    else:
        success = f"Order #{session['current_order']} has been created."

    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT mainCategory, subCategory FROM Category ORDER BY mainCategory, subCategory"
        )
        categories = cursor.fetchall()

    category_map = {}
    for category in categories:
        main_category = category["mainCategory"]
        sub_category = category["subCategory"]
        if main_category not in category_map:
            category_map[main_category] = []
        category_map[main_category].append(sub_category)

    print("Category Map:", category_map)

    selected_category = request.args.get("category")
    main_category, sub_category = None, None

    if selected_category:
        try:
            main_category, sub_category = selected_category.split("|")
        except ValueError:
            print("Invalid category format:", selected_category)

    if main_category and sub_category:
        print(f"Selected category: {main_category}, {sub_category}")
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT i.ItemID, i.iDescription, i.quantityNum
                FROM Item i
                WHERE i.mainCategory = %s AND i.subCategory = %s AND i.quantityNum > 0
                """,
                (main_category, sub_category),
            )
            items = cursor.fetchall()
            print("Items fetched:", items)

    if request.method == "POST":
        item_id = request.form["item_id"]
        requested_quantity = int(request.form["quantity"])

        with conn.cursor() as cursor:
            cursor.execute("SELECT quantityNum FROM Item WHERE ItemID = %s", (item_id,))
            item = cursor.fetchone()
            if not item or requested_quantity > item["quantityNum"]:
                error = "Not enough stock available."
            else:
                cursor.execute(
                    "SELECT quantityNum FROM ItemIn WHERE ItemID = %s AND orderID = %s",
                    (item_id, session["current_order"]),
                )
                existing_item = cursor.fetchone()

                if existing_item:
                    cursor.execute(
                        "UPDATE ItemIn SET quantityNum = quantityNum + %s WHERE ItemID = %s AND orderID = %s",
                        (requested_quantity, item_id, session["current_order"]),
                    )
                    print(f"Updated existing ItemIn entry for ItemID {item_id}.")
                else:
                    cursor.execute(
                        "INSERT INTO ItemIn (ItemID, orderID, quantityNum, found, status) VALUES (%s, %s, %s, FALSE, 'Holding')",
                        (item_id, session["current_order"], requested_quantity),
                    )
                    print(f"Inserted new ItemIn entry for ItemID {item_id}.")

                cursor.execute(
                    "UPDATE Item SET quantityNum = quantityNum - %s WHERE ItemID = %s",
                    (requested_quantity, item_id),
                )
                print(
                    f"Updated stock for ItemID {item_id} by reducing {requested_quantity}."
                )
                conn.commit()
                success = f"Added {requested_quantity} of Item #{item_id} to the order."

        if main_category and sub_category:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT i.ItemID, i.iDescription, i.quantityNum
                    FROM Item i
                    WHERE i.mainCategory = %s AND i.subCategory = %s AND i.quantityNum > 0
                    """,
                    (main_category, sub_category),
                )
                items = cursor.fetchall()
                print("Updated items fetched:", items)

    return render_template(
        "add_to_order.html",
        category_map=category_map,
        items=items,
        selected_category=selected_category,
        error=error,
        success=success,
    )


# ------------------------------------------------------------------------------
# feature 7
@app.route('/prepare_order', methods=['GET', 'POST'])
def prepare_order():
    cursor = conn.cursor()

    if request.method == 'POST':
        # Collect form data
        order_id = request.form.get('orderID')
        item_id = request.form.get('ItemID')
        quantity_num = request.form.get('quantityNum')
        room_number = request.form.get('roomNumber')
        shelf_number = request.form.get('shelfNumber')
        client_username = request.form.get('username')

        # Search by Client Username
        if client_username and not order_id:
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

        # Search by Order ID or Update Location
        if order_id:
            if not room_number:  # Search order details
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
                    ORDER BY i.ItemID, i.quantityNum
                '''
                cursor.execute(item_query, (order_id,))
                items = cursor.fetchall()

                return render_template('prepare_order.html', order=order, items=items)

            elif item_id and quantity_num:  # Update location for specific quantityNum
                try:
                    location_check_query = '''
                        SELECT COUNT(*) AS count FROM Location WHERE roomNum = %s AND shelfNum = %s
                    '''
                    cursor.execute(location_check_query, (room_number, shelf_number))
                    location_exists = cursor.fetchone()['count']

                    if not location_exists:
                        insert_location_query = '''
                            INSERT INTO Location (roomNum, shelfNum, shelf, shelfDescription)
                            VALUES (%s, %s, %s, %s)
                        '''
                        cursor.execute(insert_location_query, (room_number, shelf_number, 'Updated', 'Updated location'))
                        conn.commit()

                    # Determine the status based on the room number
                    if int(room_number) == 99:  # If moving to holding room
                        new_status = 'Holding'
                    else:  # If moving to any other room
                        new_status = 'Available'

                    # Update the location and status of the specific quantityNum
                    update_query = '''
                        UPDATE ItemIn
                        SET holdingRoomNum = %s, holdingShelfNum = %s, status = %s
                        WHERE orderID = %s AND ItemID = %s AND quantityNum = %s
                    '''
                    cursor.execute(update_query, (room_number, shelf_number, new_status, order_id, item_id, quantity_num))
                    conn.commit()

                    # Fetch updated data
                    item_query = '''
                        SELECT i.ItemID, i.quantityNum, i.status, l.roomNum, l.shelfNum, l.shelfDescription
                        FROM ItemIn i
                        LEFT JOIN Location l ON i.holdingRoomNum = l.roomNum AND i.holdingShelfNum = l.shelfNum
                        WHERE i.orderID = %s
                        ORDER BY i.ItemID, i.quantityNum
                    '''
                    cursor.execute(item_query, (order_id,))
                    items = cursor.fetchall()

                    query = 'SELECT * FROM Ordered WHERE orderID = %s'
                    cursor.execute(query, (order_id,))
                    order = cursor.fetchone()

                    return render_template('prepare_order.html', success=f"Quantity {quantity_num} of Item {item_id} updated.", order=order, items=items)

                except Exception as e:
                    conn.rollback()
                    print(f"Error updating order: {e}")
                    return render_template('prepare_order.html', error="An error occurred while updating the order. Please try again.")
    return render_template('prepare_order.html')



# ------------------------------------------------------------------------------
# feature 8
@app.route("/user_orders", methods=["GET"])
def user_orders():
    # Get the current logged-in user
    username = session.get("username")
    if not username:
        return redirect(url_for("login"))

    # Fetch all orders associated with the current user
    cursor = conn.cursor()
    query = """
        SELECT o.orderID, o.orderDate, o.orderNotes, o.supervisor, o.client
        FROM Ordered o
        LEFT JOIN Delivered d ON o.orderID = d.orderID
        WHERE o.client = %s OR d.userName = %s
    """
    cursor.execute(query, (username, username))
    orders = cursor.fetchall()
    cursor.close()

    # Render the results
    return render_template("user_orders.html", orders=orders, username=username)


print(app.url_map)

app.secret_key = "some key that you will never guess"
# Run the app on localhost port 5000
# debug = True -> you don't have to restart flask
# for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run("127.0.0.1", 5000, debug=True)
