from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
import mysql.connector

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Database configuration
host = "10.100.1.101"
user = "asjer" 
password = "myPass"
database = "weatherapp"

# Connect to the database
db = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database,
)
 
if db.is_connected():
    print("Database is connected")
else:
    print("No connection")
    

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/FAQ')
def FAQ():
    return render_template('FAQ.html')

@app.route('/userLog')
def userLog():
    return render_template('userLog.html')

@app.route('/application')
def app_function():
    username = session.get('username')
    return render_template('application.html', username=username)

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()  # Clear the entire session
    return redirect(url_for('login'))


@app.route('/signUp', methods=['POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            cursor = db.cursor()

            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert user data into the database using placeholders
            insert_query = "INSERT INTO user (username, password) VALUES (%s, %s)"
            user_data = (username, hashed_password)
            cursor.execute(insert_query, user_data)

            db.commit()
            cursor.close()

            # Redirect to the login page after successful registration
            return redirect(url_for('login'))

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return render_template('signUp.html', msg='Registration failed')


@app.route('/login', methods=['POST'])
def log_in():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            cursor = db.cursor(buffered=True)

            # Select user data from the database using placeholders
            select_query = "SELECT * FROM user WHERE username = %s"
            user_data = (username,)
            cursor.execute(select_query, user_data)
            
            user = cursor.fetchone()  # Fetch the first row of the result
            cursor.close()

            if user:
                hashed_password = user[2]  # Get the hashed password from the result
                if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                    session['username'] = username  # Store username in session
                    # Redirect to the application page after successful login
                    return redirect(url_for('app_function'))
                else:
                    return render_template('login.html', msg='Login failed')
            else:
                return render_template('login.html', msg='Login failed')

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return render_template('login.html', msg='Login failed')
                
        
        

if __name__ == '__main__':
    app.run(debug=True)
