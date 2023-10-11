from flask import Flask, request, render_template, redirect, url_for
import psycopg2

app = Flask(__name__)

# PostgreSQL database configuration
db_params = {
    'database': 'cs699_pdb',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',  # Change this if your database is hosted elsewhere
    'port': '5432'        # Default PostgreSQL port
}

@app.route('/')
def login():
    return render_template('index.html')

@app.route('/auth', methods=['POST'])
def authenticate():
    username = request.form['username']
    password = request.form['password']

    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()

    # Query the database to check user credentials (this is a simplified example) 
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
        # Successful login
        return "Login successful"
    else:
        # Failed login
        return "Login failed"

if __name__ == '__main__':
    app.run(debug=True)
