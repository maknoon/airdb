#!~/usr/bin/python
from flask import Flask, flash, request, render_template, session
from airplanedb import AirplaneDb
import config
import hashlib
import json

app = Flask(__name__)
app.secret_key = hashlib.sha224('oooh so secure').hexdigest()
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
        return render_template('db.html', type='user')

    elif session.get('type') == 'admin':
        # get all airports
        get_airports = json.loads(airdb.get_airport(None).get_data())
        print(get_airports['airport'])
        data_to_display = get_airports['airport']
        return render_template('db.html', type='admin', data=data_to_display)

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
    added = airdb.add_customer(cust_name,
        request.args.get('age'), request.args.get('email'),
        request.args.get('phone'))

    return 'ADDED NEW CUSTOMER %s WITH ID %d' % (cust_name, added)

# test update customer
# @app.route('/customerupdate')
# def update_customer():
#     req_body = request.get_json()
#     cust_id = request.args.get('id')
#     customer = airdb.get_customer(cust_id)
#     if (customer == 0): abort(404)
#     else:
#         if "phone" in req_body:
#             newphone = req_body["phone"]
#             airdb.update_customer(cust_id, 'C_PHONE', newphone)
#         if "email" in req_body:
#             newemail = req_body["email"]
#             airdb.update_customer(cust_id, 'C_EMAIL', newemail)
#         if "name" in req_body:
#             newname = req_body["name"]
#             airdb.update_customer(cust_id, 'C_NAME', newname)
#     customer = airdb.update_customer(cust_id)
#     customer_json = {"id":user[0],"name":user[1],"age":user[2],
#                     "email":user[3],"phone_number":user[4]}
#     res_body = json.dumps(customer_json, indent=4, separators=(',', ': '))

#     return res_body


# test add new frequent flier
@app.route('/ff')
def add_frequent_flier():
    airdb.add_frequent_flier(request.args.get('id'))

    return 'WELCOME TO THE FREQUENT FLIER CLUB'

# test add baggage
@app.route('/baggage')
def add_baggage():
    airdb.add_baggage(request.args.get('id'),
        request.args.get('weight'))

    return 'ADDED BAGGAGE'

# @app.route('/ffupdate')
# def update_frequent_flier():
#     cust_id = request.args.get('id')
#     miles = request.args.get('miles')
#     airdb.update_frequent_flier(cust_id, miles)

#     return 'ADDED %s MILES TO ACCOUNT' % miles

# Add airport route
@app.route('/airport/newairport')
def add_airport():
    msg = airdb.add_airport(request.args.get('id'),
        request.args.get('city'), request.args.get('country'))

    return msg

# Add airport route
@app.route('/airport/getairport')
def get_airport():
    apid = request.args.get('id')
    data = airdb.get_airport(apid)

    return data

# Add airport route
@app.route('/airport/delete')
def delete_airport():
    apid = request.args.get('id')
    data = airdb.delete_airport(apid)

    return data

# Add airport route
@app.route('/airport/update')
def update_airport():
    apid = request.args.get('id')
    data = airdb.update_airport(apid, request.args.get('city'),
         request.args.get('country'), request.args.get('newcity'),
         request.args.get('newcountry'))

    return data


# ---------------------------------------------------------
# SERVE THE APP
# ---------------------------------------------------------

if __name__ == '__main__':
    print('Connecting to db...{}'.format(config.dbname))

    app.run()

