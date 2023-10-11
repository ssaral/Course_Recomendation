from flask import Flask, request, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)

# PostgreSQL database configuration
db_params = {
    'database': 'cs699_pdb',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',  
    'port': '5432'       
}

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    # To connect to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Querying the database to check user credentials
    try:
        check_login_script = 'SELECT * FROM user_login_table WHERE username = %s AND password = %s'
        cursor.execute( check_login_script, (username, password))
        user = cursor.fetchall()
        print("Checking value of user", cursor.fetchall()) 
    except Exception as e:
        print("Error executing SQL query:", str(e))

    cursor.close()
    conn.close()

    if user:
        # For Successful login redirecting to choose stream page.
        print("Login successfull for", user[0][0])
        return redirect(url_for('choose_stream'))
    else:
        # Failed login
        print("Login failed for", user[0])
        return "Login failed"
        
@app.route('/choose_your_stream')
def choose_stream():
    return render_template('stream_selection.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/register', methods=['POST'])
def register():
    username = request.form['username']
    password = request.form['password']

    # To connect to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    #Checking if user already exists
    cursor.execute("SELECT username FROM user_login_table WHERE username = %s or password = %s", (username, password))
    flag = cursor.fetchone() 
    print("flag ki value", flag) 
    if flag:
    	cursor.close()
    	conn.close()
    	return render_template('signup.html', alert_message="Username is already taken. Please choose another username.")
    	#return redirect(url_for('/')) 
    else:
    	# Inserting new user into the database
    	cursor.execute("INSERT INTO user_login_table (username, password) VALUES (%s, %s)", (username, password))
    	conn.commit()
    	cursor.close()
    	conn.close()
    	
    	# Redirect to the choose page after successful registration
    	#return redirect(url_for('login'))
    	return render_template('signup.html', alert_message="Account created. Kindly procced by clicking on login page.")

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_pwd():
	password=None
	if request.method == 'POST':
	    username = request.form['username']

	    # To connect to the PostgreSQL database
	    conn = psycopg2.connect(**db_params)
	    cursor = conn.cursor()
	    
	    #fetching password for that user. // NOTE: username, //
	    cursor.execute("SELECT password FROM user_login_table WHERE username = %s", (username,))
	    flag = cursor.fetchone() 
	    print("flag ki value", flag) 
	    if flag:
	    	print("password wala flag: ", flag)
	    	password=flag[0]
	    	print("passwaor ki value is", password)
	    	cursor.close()
	    	conn.close()
	    else:
	    	cursor.close()
	    	conn.close()
	    	# Redirect to the same page if user not found.
	    	return render_template('forgot_password.html', error_message="User not found. Kindly create a new account or enter valid username.")
	
	# Redirect to the same page if user found and display password
	return render_template('forgot_password.html', password=password)

    
@app.route('/under-construction')
def under_construction():
    return render_template('under_construction.html')

if __name__ == '__main__':
    app.run(debug=True)

