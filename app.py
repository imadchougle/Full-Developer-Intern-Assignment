from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Imadchougle@4056'
app.config['MYSQL_DB'] = 'form_db'

mysql = MySQL(app)

SENDER_EMAIL = 'tempforassignment@gmail.com'
SENDER_PASSWORD = 'scflzerxrwcdydup'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        password = request.form['password']
        email = request.form['email']
        city = request.form['city']
        country = request.form['country']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        user = cursor.fetchone()

        if user:
            if user[7] == False:  # Assuming user[7] indicates verified status
                # User is not verified; update details and redirect to OTP verification
                otp = random.randint(100000, 999999)
                session['otp'] = otp
                session['email'] = email

                send_otp(email, otp)

                cursor.execute(''' UPDATE users SET name = %s, phone = %s, password = %s, city = %s, country = %s
                                   WHERE email = %s ''', (name, phone, password, city, country, email))
                mysql.connection.commit()
                cursor.close()

                return redirect(url_for('verify_otp'))
            else:
                # User is already verified; show popup
                return render_template('register.html', already_registered=True, email=email)
        else:
            # New user; lets proceed with registration
            otp = random.randint(100000, 999999)
            session['otp'] = otp
            session['email'] = email

            send_otp(email, otp)

            cursor.execute(''' INSERT INTO users(name, phone, password, email, city, country, verified)
                              VALUES(%s, %s, %s, %s, %s, %s, %s) ''', (name, phone, password, email, city, country, False))
            mysql.connection.commit()
            cursor.close()

            return redirect(url_for('verify_otp'))
    return render_template('register.html', already_registered=False)


@app.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    if request.method == 'POST':
        user_otp = request.form['otp']
        if int(user_otp) == session['otp']:
            cursor = mysql.connection.cursor()
            cursor.execute('UPDATE users SET verified = %s WHERE email = %s', (True, session['email']))

            # Fetch user details for the global contacts insertion
            cursor.execute('SELECT name, phone FROM users WHERE email = %s', (session['email'],))
            user = cursor.fetchone()
            name, phone = user

            cursor.execute('''INSERT INTO global_contacts (phone, name)
                              VALUES (%s, %s)
                              ON DUPLICATE KEY UPDATE name = VALUES(name)''', (phone, name))

            mysql.connection.commit()
            cursor.close()
            return jsonify({'isValid': True, 'message': 'Verified successfully, redirecting to login page...'})
        else:
            return jsonify({'isValid': False, 'message': 'Invalid OTP. Please try again.'})
    return render_template('verify_otp.html')



def send_otp(receiver_email, otp):
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp}'

    msg = MIMEMultipart()
    msg['From'] = SENDER_EMAIL
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(SENDER_EMAIL, SENDER_PASSWORD)
    server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
    server.quit()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE email = %s AND password = %s AND verified = %s', (email, password, True))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['logged_in'] = True
            session['user_id'] = user[0]
            session['name'] = user[1]
            session['city'] = user[5]
            session['country'] = user[6]
            return jsonify({'isValid': True, 'message': 'Logged in successfully, redirecting...'})
        else:
            return jsonify({'isValid': False, 'message': 'Invalid credentials or account not verified'})
    return render_template('login.html')


@app.route('/welcome', methods=['GET', 'POST'])
def welcome():
    if 'logged_in' in session:
        search_results = None

        if request.method == 'POST':
            if 'contact_name' in request.form and 'contact_phone' in request.form:
                # Adding a new contact
                contact_name = request.form['contact_name']
                contact_phone = request.form['contact_phone']

                cursor = mysql.connection.cursor()
                cursor.execute('INSERT INTO contacts(user_id, name, phone) VALUES(%s, %s, %s)',
                               (session['user_id'], contact_name, contact_phone))
                cursor.execute('''INSERT INTO global_contacts (phone, name)
                                  VALUES (%s, %s)
                                  ON DUPLICATE KEY UPDATE name = VALUES(name)''', (contact_phone, contact_name))
                mysql.connection.commit()
                cursor.close()
            elif 'search_query' in request.form and 'search_by' in request.form:
                # Performing a search
                search_query = request.form['search_query']
                search_by = request.form['search_by']

                cursor = mysql.connection.cursor()
                if search_by == 'name':
                    cursor.execute('''SELECT phone, name, spam_likelihood FROM global_contacts
                                      WHERE name LIKE %s
                                      ORDER BY
                                      CASE
                                          WHEN name LIKE %s THEN 1
                                          ELSE 2
                                      END''', (f"%{search_query}%", f"{search_query}%"))
                elif search_by == 'phone':
                    cursor.execute('SELECT phone, name, spam_likelihood FROM global_contacts WHERE phone LIKE %s', (f"%{search_query}%",))

                search_results = cursor.fetchall()
                cursor.close()

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT name, phone FROM contacts WHERE user_id = %s', (session['user_id'],))
        contacts = cursor.fetchall()
        cursor.close()

        return render_template('welcome.html', name=session['name'], city=session['city'], country=session['country'], contacts=contacts, search_results=search_results)
    else:
        return redirect(url_for('login'))


@app.route('/mark_spam', methods=['POST'])
def mark_spam():
    if 'logged_in' in session:
        spam_phone = request.form['spam_phone']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT phone FROM global_contacts WHERE phone = %s', (spam_phone,))
        global_contact = cursor.fetchone()

        if global_contact:
            cursor.execute('UPDATE global_contacts SET spam_likelihood = spam_likelihood + 1 WHERE phone = %s', (spam_phone,))
        else:
            cursor.execute('INSERT INTO global_contacts (phone, name, spam_likelihood) VALUES (%s, %s, %s)',
                           (spam_phone, 'nulluser', 1))

        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('welcome'))
    else:
        return redirect(url_for('login'))


@app.route('/details', methods=['GET', 'POST'])
def details():
    if request.method == 'POST':
        phone = request.form['phone']  # Getimg phone number from form submission
    else:
        phone = request.args.get('phone')  # Alternatively, we get phone from query parameters if using GET

    cursor = mysql.connection.cursor()

    # Query to fetch contact details from global_contacts based on phone number
    cursor.execute('SELECT phone, name, spam_likelihood FROM global_contacts WHERE phone = %s', (phone,))
    contact_details = cursor.fetchall()  # Fetchng all rows matching the query

    user_email = None

    if 'logged_in' in session:
        # Query to check if the phone number belongs to a contact of the logged-in user
        cursor.execute('SELECT user_id FROM contacts WHERE phone = %s AND user_id = %s', (phone, session['user_id']))
        user_contact = cursor.fetchone()  # Fetch the result of the qry

        if user_contact:
            # If the phone number is a contact of the logged-in user, fetch their email
            cursor.execute('SELECT email FROM users WHERE phone = %s', (phone,))
            user_email = cursor.fetchone()  # Fetchng the user's email associated with the phone number

    cursor.close()

    return render_template('details.html', contact_details=contact_details, user_email=user_email)



@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    session.pop('user_id', None)
    session.pop('name', None)
    session.pop('city', None)
    session.pop('country', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)