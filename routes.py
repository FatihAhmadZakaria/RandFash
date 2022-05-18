from typing import final
from myweb import app
from flask import Flask, redirect, render_template, request, session, url_for, flash
from flask_mysqldb import MySQL
import re
from passlib.hash import sha256_crypt

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'onlineshop'
mysql = MySQL(app)

@app.route('/')
def home():
    return render_template('beranda.html')
@app.route('/hometest')
def hometest():
    return render_template('hometest.html')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        pw = request.form['password']
        cur = mysql.connection.cursor()
        result = cur.execute('SELECT pass FROM pengguna WHERE username = %s', (username,))
        if result > 0:
            # Get stored value
            data = cur.fetchone()
            password = data[0]

            # Compare password
            if sha256_crypt.verify(pw, password):
                # passed
                session['logged_in'] = True

                return redirect(url_for('home'))

            else:
                flash('Incorrect password', 'danger')
                return render_template('login.html')

        else:
            flash('Username not found', 'danger')
            # Close connection
            cur.close()
            return render_template('login.html')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/registeruser', methods =['GET', 'POST'])
def registeruser():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = sha256_crypt.encrypt(str(request.form['password']))
        email = request.form['email']
        nama = request.form['nama']
        tgl = request.form['tgl']
        alamat = request.form['alamat']
        nohp = request.form['nohp']
        gen = request.form['gen']
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM pengguna WHERE username = % s', (username, ))
        account = cur.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cur.execute('INSERT INTO pengguna(nama, tgl, gender, username, email, pass, alamat, nmrhp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)', (nama, tgl, gen, username, email, password, alamat, nohp))
            mysql.connection.commit()
            # msg = 'You have successfully registered !'
            return redirect(url_for('login'))
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg = msg)