from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from settings import FOLDER_PATH, DB_NAME, USER_NAME, PASSWORD, HOST, TABLE, MAILID, MAIL_PORT, MAIL_PASSWORD, MAIL_SERVER
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__, template_folder=FOLDER_PATH)
app.secret_key = 'test'

def get_db_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER_NAME,
        password=PASSWORD,
        database=DB_NAME
    )

@app.route('/')
def dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = f"SELECT * FROM {TABLE}"
    cursor.execute(query) 
    entries = cursor.fetchall()
    conn.close()
    return render_template('dashboard.html', entries=entries)

@app.route('/send_email', methods=['GET', 'POST'])
def send_email():
    if request.method == 'POST':
        target_email = request.form['email']
        subject = "Security Alert: Phishing Simulation"
        body =  f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            line-height: 1.6;
                        }}
                        .container {{
                            max-width: 600px;
                            margin: auto;
                            border: 1px solid #ddd;
                            padding: 20px;
                            background-color: #f9f9f9;
                        }}
                        .header {{
                            background-color: #0070ba;
                            color: white;
                            padding: 10px;
                            text-align: center;
                            font-size: 20px;
                        }}
                        .content {{
                            margin: 20px 0;
                        }}
                        .button {{
                            display: inline-block;
                            margin-top: 20px;
                            padding: 10px 20px;
                            background-color: #0070ba;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                        }}
                        .button:hover {{
                            background-color: #005c99;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">PayPal Notification</div>
                        <div class="content">
                            <p>Dear User,</p>
                            <p>
                                We noticed unusual login activity on your PayPal account. To ensure the safety 
                                of your account, please verify your login details immediately.
                            </p>
                            <p>
                                If you do not verify within 24 hours, your account will be temporarily locked 
                                for security purposes.
                            </p>
                            <center><a href="http://127.0.0.1:5500/login" class="button" style="color:white">Verify Your Account</a><center>
                        </div>
                        <div class="footer">
                            <p style="font-size: 12px; color: #666;">This is a simulated phishing attempt for educational purposes.</p>
                        </div>
                    </div>
                </body>
            </html>
            """
        
        send_phishing_email(target_email, subject, body)
        return redirect(url_for('dashboard'))
    return render_template('send_email.html')

def send_phishing_email(target_email, subject, body):
    sender_email = MAILID
    receiver_email = target_email
    password = MAIL_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    try:
        with smtplib.SMTP(MAIL_SERVER, port=MAIL_PORT) as server:
            server.starttls()
            server.login(sender_email, password)
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
            print(f"Phishing email sent to {target_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    app.run(debug=True)
