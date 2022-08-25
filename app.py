
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import hashlib
from datetime import timedelta
import re



app = Flask(__name__)

#this secret key is used for sessions, it keeps the client side sessions secure
app.secret_key = 'secretkey123'

# database information
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password1905'
app.config['MYSQL_DB'] = 'flaskdb'
#app.config['SECRET_KEY'] = 'secretkey123'

# app içine tanımlanan config bilgileri mysql değişkenine atanıyor
mysql = MySQL(app)

# if bcrypt.hashpw(password, account['password'].encode('utf-8')) == account['password'].encode('utf-8'):

#get message is send server returns data(retrieve information from server), post is used to send html form data to server
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])  #page works with both POST and GET requests 
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password'].encode('utf-8') #8-bit valu encoding
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor) #cursor enables to interact with database table, it scans data and execute sql queries
        print(username, hashlib.md5(password).hexdigest())
        cursor.execute('SELECT * FROM usertable WHERE username = % s AND password = % s',  (username, hashlib.md5(password).hexdigest()))
        user = cursor.fetchone()  #type dictionary 
        print(type(user))
        if user:
            #setting encrypted cookies(sessions)
            session['loggedin'] = True
            session['id'] = user['id']
            session['username'] = user['username']
            session.permanent=True
            app.permanent_session_lifetime=timedelta(minutes=1)
            return redirect(url_for('home'))
          
            return render_template("index.html", message=message)
        else:
            message = 'Incorrect username or password!'
    return render_template("index.html",message=message)


@app.route('/logout')
def logout():
    session.pop('loggedin', None) #session.pop clear the users session data when the user logs out
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))



@app.route('/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username = request.form['username']
        password = request.form['password'].encode('utf-8')
        hash_password = hashlib.md5(password).hexdigest()
        email = request.form['email']

        # Check if user exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usertable WHERE username = % s', (username, ))

        cursor_email = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor_email.execute( 'SELECT * FROM usertable WHERE email = % s', (email, ))
        # Fetch one record and return result
        user = cursor.fetchone()
        print(type(user))
        # If account exists in usertable table in our database
        
        if user:
            message = 'This username already exists!'
        elif cursor_email.fetchone():
            message = 'E-mail already in usage'
        elif not email or not username:
            message = 'Please fiil out the form'
        else:
            cursor.execute('INSERT INTO usertable VALUES (NULL, % s, % s, % s)', (username, hash_password, email, ))
        
            mysql.connection.commit()     # Yapılan değişikleri kaydetmek ve veritabında uygulamak için gerekli olan commit fonksiyonu. Since mysql is not a auto-commit DB, it shoulde be done manually
            message = 'You have successfully registered!'

    return render_template("register.html", message=message)




@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM usertable WHERE id = %s', (session['id'],))
        user = cursor.fetchone()
    
        return render_template('profile.html', user=user)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))




@app.route('/delete', methods=['GET', 'POST'])
def delete():   
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST': 
        for id in request.form.getlist('mycheckbox'):
            print(id)
            cursor.execute('DELETE FROM usertable WHERE id = {0}'.format(id))
            mysql.connection.commit()
        flash('Successfully Deleted!')
    return redirect('/users')


@app.route('/users', methods =["GET"])
def users():
 if 'loggedin' in session:
    cursor = mysql.connection.cursor()
    numberOfUser = cursor.execute("SELECT * FROM usertable")
    if numberOfUser > 0:
        userInformation = cursor.fetchall() #fetchall sorgu resultunı okur ve değişkene atıyor bu satırda class, tuple variable
        print(type(userInformation))
        print(userInformation)
        print(numberOfUser)
        return render_template("users.html",userInformation=userInformation)

    else:
        return "there is no user logged in yet!"

 else:
    return "you have to logged-in first to see users table"








@app.errorhandler(404)
def error(e):
    return render_template("404.html")



if __name__ == '__main__':
    app.run(debug=True)
