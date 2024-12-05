#Import Flask Library
from flask import Flask, render_template, request, session, url_for, redirect, flash
import pymysql.cursors

#for uploading photo:
from app import app
#from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


###Initialize the app from Flask
##app = Flask(__name__)
##app.secret_key = "secret key"

#Configure MySQL
conn = pymysql.connect(host='localhost',
                       port=3306,
                       user='root',
                       password='root',
                       db='FlaskDemo',
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

        # if data['role'] == 'staff':
        #   return redirect(url_for('home_staff'))
        # if data['role'] == 'client':
        #   return redirect(url_for('home_client'))
        # if data['role'] == 'donor':
        #   return redirect(url_for('home_donor'))
        # if data['role'] == 'volunteer':
        #   return redirect(url_for('home_volunteer'))

        return redirect(url_for('home'))
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
    fname = request.form['first_name']
    lname = request.form['last_name']
    email = request.form['email']
    role = request.form['role']

    if(not username or not password or not email):
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
        ins = 'INSERT INTO user VALUES(%s, %s)'
        cursor.execute(ins, (username, password, fname, lname, email))
        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/person')
def home():
    user = session['username']
    return render_template('person.html', username=user)

# @app.route('/home_staff')
# def home_staff():
#     return render_template('home_staff.html', username = session['username'])
# @app.route('/home_client')
# def home_client():
#     return render_template('home_client.html', username = session['username'])
# @app.route('/home_donor')
# def home_donor():
#     return render_template('home_donor.html', username = session['username'])
# @app.route('/home_volunteer')
# def home_volunteer():
#     return render_template('home_volunteer.html', username = session['username'])

@app.route('/action_find_item', methods=['GET'])
def find_item():
    itemID = request.args['itemID']
    cursor = conn.cursor()
    # a query to find the pieces of the item and their locations
    query = ''
    cursor.execute(query, itemID)
    pieces = cursor.fetchall()
    cursor.close()
    return render_template('find_item.html', itemID=itemID, pieces=pieces)

@app.route('/action_find_order', methods=['GET'])
def find_order():
    orderID = request.args['orderID']
    cursor = conn.cursor()
    # a query to find items in the order along with pieces and their locations
    query = ''
    cursor.execute(query, orderID)
    items = cursor.fetchall()
    cursor.close()
    return render_template('find_order.html', orderID=orderID, items=items)

@app.route('/action_accept_donation', methos=['GET'])
def accept_donation():
    username = request.form['username']
    cursor = conn.cursor()
    # a query to find the user
    query = ''
    cursor.execute(query, itemID)
    user = cursor.fetchone()
    if user['role'] != 'donor':
        error = 'This user is not a donor'
        return render_template('person.html', error=error)
    cursor.close()
    return render_template('accept_donation.html', username=user['userName'])

@app.route('/post', methods=['GET', 'POST'])
def post():
    username = session['username']
    cursor = conn.cursor();
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
    cursor = conn.cursor();
    query = 'SELECT ts, blog_post FROM blog WHERE username = %s ORDER BY ts DESC'
    cursor.execute(query, poster)
    data = cursor.fetchall()
    cursor.close()
    return render_template('show_posts.html', poster_name=poster, posts=data)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/', methods=['POST'])
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


@app.route('/logout')
def logout():
    session.pop('username')
    return redirect('/')
        
app.secret_key = 'some key that you will never guess'
#Run the app on localhost port 5000
#debug = True -> you don't have to restart flask
#for changes to go through, TURN OFF FOR PRODUCTION
if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug = True)
