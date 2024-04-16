from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Database configuration
host = "10.2.2.223"
user = "root"
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

            # Insert user data into the database using placeholders
            insert_query = "INSERT INTO user (username, password) VALUES (%s, %s)"
            user_data = (username, password)
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
            select_query = "SELECT * FROM user WHERE username = %s AND password = %s"
            user_data = (username, password)
            cursor.execute(select_query, user_data)
            
            user = cursor.fetchone()  # Fetch the first row of the result
            cursor.close()

            if user:
                session['username'] = username  # Store username in session
                # Redirect to the application page after successful login
                return redirect(url_for('app_function'))
            else:
                return render_template('login.html', msg='Login failed')

        except mysql.connector.Error as err:
            print("Something went wrong: {}".format(err))
            return render_template('login.html', msg='Login failed')

if __name__ == '__main__':
    app.run(debug=True)
