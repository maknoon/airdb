#!~/usr/bin/python
from flask import Flask
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
    return 'airdb'

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

# test update customer
@app.route('/customerupdate')
def update_customer():
    req_body = request.get_json()
    cust_id = request.args.get('id')
    customer = airdb.get_customer(cust_id)
    if (customer==0): abort(404)
    else:
        if "phone" in req_body:
            newphone = req_body["phone"]
            airdb.update_customer(cust_id, 'C_PHONE', newphone)
        if "email" in req_body:
            newemail = req_body["email"]
            airdb.update_customer(cust_id, 'C_EMAIL', newemail)
        if "name" in req_body:
            newname = req_body["name"]
            airdb.update_customer(cust_id, 'C_NAME', newname)
    customer = airdb.get_customer(cust_id)
    customer_json = {"id":user[0],"name":user[1],"age":user[2],
                    "email":user[3],"phone_number":user[4]}
    res_body = json.dumps(customer_json, indent=4, separators=(',', ': '))

    return res_body


# test add new frequent flier
@app.route('/ff')
def add_frequent_flier():
    cust_id = request.args.get('id')
    miles = 0
    #miles initialized to 0
    airdb.add_frequent_flier(cust_id, miles)

    return 'WELCOME TO THE FREQUENT FLIER CLUB'


# test add baggage
@app.route('/baggage')
def add_baggage():
    cust_id = request.args.get('id')
    baggage_ID = request.args.get('bid')
    airdb.add_baggage(cust_id, baggage_ID)

    return 'ADDED BAGGAGE'

@app.route('/ffupdate')
def update_frequent_flier():
    cust_id = request.args.get('id')
    miles = request.args.get('miles')
    airdb.update_frequent_flier(cust_id, miles)
    
    return 'ADDED %s MILES TO ACCOUNT' % miles


# ---------------------------------------------------------
# SERVE THE APP
# ---------------------------------------------------------

if __name__ == '__main__':
    print('Connecting to db...{}'.format(config.dbname))
    app.secret_key = os.urandom(12)
    app.run()
