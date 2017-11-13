#!~/usr/bin/python
from flask import Flask, flash, request, render_template, session
from airplanedb import AirplaneDb
import config
import os

app = Flask(__name__)
airdb = AirplaneDb(host=config.host,
                   user=config.dbusr,
                   pw=config.dbpwd,
                   db=config.dbname)

# ---------------------------------------------------------
# HOME
# ---------------------------------------------------------

@app.route('/')
def index():
    if session.get('type') == 'user':
        return 'Logged in as user!'
    elif session.get('type') == 'admin':
        return 'Logged in as admin!'
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if request.form['password'] == config.adminpwd and request.form['username'] == 'admin':
        session['type'] = 'admin'
    elif request.form['password'] == config.userpwd and request.form['username'] == 'user':
        session['type'] = 'user'
    else:
        flash('wrong password!')
    return index()

@app.route('/logout')
def logout():
    session['type'] = 'none'
    return index()

@app.route('/test/<name>')
def test_name(name):
    return 'Welcome, {}!'.format(name)


# ---------------------------------------------------------
# DATABASE ENDPOINTS
# ---------------------------------------------------------
# reset the database
@app.route('/reset')
def reset():
    airdb.reset_db()
    airdb.populate_db()
    return 'DB HAS BEEN RESET AND POPULATED'

# test create new customer
@app.route('/customer')
def add_customer():
    cust_name = request.args.get('name')
    cust_age = request.args.get('age')
    cust_email = request.args.get('email')
    cust_phone = request.args.get('phone')

    airdb.add_customer(cust_name, cust_age, cust_email, cust_phone)

    return 'ADDED NEW CUSTOMER %s' % cust_name


if __name__ == '__main__':
    print('Connecting to db...{}'.format(config.dbname))
    app.secret_key = os.urandom(12)
    app.run()
