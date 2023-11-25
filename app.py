from flask import Flask, request, render_template, redirect, url_for, Response
import psycopg2
import io
import csv

app = Flask(__name__)

# PostgreSQL database configuration
db_params = {
    'database': 'cs699_pdb',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',  
    'port': '5432'       
}

# Index Page
@app.route('/')
def login():
    return render_template('index.html')

# Authentication Logic
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
        print("Login successfull for", user)
        return redirect(url_for('choose_stream'))
    else:
        # Failed login
        print("Login failed for", user)
        #return "Login failed"
        return render_template('index.html', error_message="User and/or Password is incorrect. Kindly create a new account or Enter valid Username and Password.") 

# Choosing Stream logic
@app.route('/choose_your_stream')
def choose_stream():
    return render_template('stream_selection.html')

# SignUp Logic
@app.route('/signup')
def signup():
    return render_template('signup.html')

# Register Logic
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

# Forget Password Logic
@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_pwd():
	password=None #if-else mai use kar raha hu and then return mai if user is found. 
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
	    	print("password ki value is", password)
	    	cursor.close()
	    	conn.close()
	    else:
	    	cursor.close()
	    	conn.close()
	    	# Redirecting to the same page if user not found.
	    	return render_template('forgot_password.html', error_message="User not found. Kindly create a new account or enter valid username.")
	
	# Redirecting to the same page if user found and display password
	return render_template('forgot_password.html', password=password)


# Under Construction Logic
@app.route('/under-construction')
def under_construction():
    return render_template('under_construction.html')


# Computer Science Logic
@app.route('/computer-science', methods=['GET','POST'])
def comp_science():
    result = None

    if request.method == 'POST':
        selected_option = request.form['role']
        print("selected option will be displayed here", selected_option)        
        # To connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()

        selected_option = selected_option.lower()
        
        # Use a parameterized query
        query = "SELECT * FROM courses_mit WHERE tags && %s"
        # Execute the query with the variable as a parameter
        cursor.execute(query, ([selected_option],))
        
        result = cursor.fetchall() 
        
        cursor.close()
        conn.close()

        print(result)
        # print(result[0])
        

    return render_template('comp_science.html', result=result)

'''
Download CSV LOGIC
@app.route('/download-csv', methods=['POST'])
def download_csv():
    result = None

    if request.method == 'POST':
        selected_option = request.form['role']
        print("role2 value in download csv", selected_option)        
        # To connect to the PostgreSQL database
        conn = psycopg2.connect(**db_params)
        cursor = conn.cursor()
        
        cursor.execute("SELECT title, url, title FROM course_description")  # WHERE keyword = %s", (selected_option,))
        result = cursor.fetchall() 
        cursor.close()
        conn.close()
        
        # Create a CSV string from the query result
        csv_data = "Title,URL,Description\n"
        for row in result:
            csv_data += f"{row[0]},{row[1]},{row[2]}\n"
        
        # Create a Flask response with the CSV data
        print(csv_data)
        response = Response(csv_data, content_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=courses.csv"
        

    return render_template('comp_science.html')
'''

if __name__ == '__main__':
    app.run(debug=True)

