#!~/usr/bin/python
from flask import Flask, abort, flash, request, render_template, session
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


# ---------------------------------------------------------
# DATABASE ENDPOINTS
# ---------------------------------------------------------

# reset the database
@app.route('/reset')
def reset():
    airdb.reset_db()
    airdb.populate_db()
    return 'DB HAS BEEN RESET AND POPULATED'

# Handle customer endpoint
@app.route('/customer', methods=['POST','PATCH','GET'])
def customer_route():
    cust_id = request.args.get('id')

    # fetch a customer by id
    if request.method == 'GET':
        customer = airdb.get_customer(cust_id)
        if customer == 0: abort(404)
        else:
            customer_json = {'id':cust_id,'name':customer[1],'age':customer[2],
                        'email':customer[3],'phone':customer[4]};
            res_body = json.dumps(customer_json, indent=4, separators=(',', ': '))

    # add a new customer
    elif request.method == 'POST':
        req_body = request.get_json()
        cust_name = req_body['name']
        added = airdb.add_customer(cust_name, req_body['age'], req_body['email'],
            req_body['phone'])

        res_body = 'ADDED NEW CUSTOMER {0} WITH ID {1}'.format(cust_name, added)

    # update a customer
    elif request.method == 'PATCH':
        req_body = request.get_json()
        customer = airdb.get_customer(cust_id)
    
        if customer == 0: abort(404)
        else:
            if 'phone' in req_body:
                newphone = '"{}"'.format(req_body['phone'])
                airdb.update_customer(cust_id, 'C_PHONE', newphone)
            if 'email' in req_body:
                newemail = '"{}"'.format(req_body['email'])
                airdb.update_customer(cust_id, 'C_EMAIL', newemail)
            if 'age' in req_body:
                newage = req_body['age']
                airdb.update_customer(cust_id, 'C_AGE', newage)
            if 'name' in req_body:
                newname = '"{}"'.format(req_body['name'])
                airdb.update_customer(cust_id, 'C_NAME', newname)

            customer = airdb.get_customer(cust_id)
            customer_json = {'id':cust_id,'name':customer[1],'age':customer[2],
                        'email':customer[3],'phone':customer[4]};
            res_body = json.dumps(customer_json, indent=4, separators=(',', ': '))

    return res_body

# test add new frequent flier
@app.route('/ff/new')
def add_frequent_flier():
    data = airdb.add_frequent_flier(request.args.get('id'))

    return data

# test add baggage
@app.route('/baggage/new')
def add_baggage():
    data = airdb.add_baggage(request.args.get('id'),
        request.args.get('weight'))

    return data

# @app.route('/ffupdate')
# def update_frequent_flier():
#     cust_id = request.args.get('id')
#     miles = request.args.get('miles')
#     airdb.update_frequent_flier(cust_id, miles)

#     return 'ADDED %s MILES TO ACCOUNT' % miles

# Handle airport endpoint
@app.route('/airport', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def airport_route():
    apid = request.args.get('id')

    # fetch a airport by id
    if request.method == 'GET':
        airport = airdb.get_airport(apid)
        if airport == 0: abort(404)
        else:
            airport_json = {'id':apid,'city':airport[1],
                            'country':airport[2]}
            res_body = json.dumps(airport_json, indent=4, separators=(',', ': '))

    # add a new airport
    elif request.method == 'POST':
        req_body = request.get_json()
        apid = req_body['id']
        res_body = airdb.add_airport(apid, req_body['city'], req_body['country'])

    # update an airport
    elif request.method == 'PATCH':
        req_body = request.get_json()
        airport = airdb.get_airport(apid)
    
        if airport == 0: abort(404)
        else:
            if 'country' in req_body:
                newcountry = '"{}"'.format(req_body['country'])
                airdb.update_airport(apid, 'AP_COUNTRY', newcountry)
            if 'city' in req_body:
                newcity = '"{}"'.format(req_body['city'])
                airdb.update_airport(apid, 'AP_CITY', newcity)
            airport = airdb.get_airport(apid)
            airport_json = {'id':apid,'city':airport[1],
                            'country':airport[2]}
            res_body = json.dumps(airport_json, indent=4, separators=(',', ': '))

    # delete an airport
    elif request.method == 'DELETE':
        res_body = airdb.delete_airport(apid)

    return res_body


# Get gates of airport route
@app.route('/gate/getOfAirport')
def get_gates_of_airport():
    apid = request.args.get('id')
    data = airdb.get_gates_of_airport(apid)

    return data

# Delete a gate route
@app.route('/gate/delete')
def delete_gate():
    apid = request.args.get('ap_id')
    gid = request.args.get('g_id')
    data = airdb.delete_gate(apid, gid)

    return data

# Get schedule of ITINERARY
@app.route('/schedule/getForItinerary')
def get_schedule_for_itinerary():
    iid = request.args.get('id')
    data = airdb.get_schedule_for_itinerary(iid)

    return data

# Add a schedule route
@app.route('/schedule/add')
def add_schedule():
    iid = request.args.get('i_id')
    fid = request.args.get('f_id')
    data = airdb.add_schedule(iid, fid)

    return data

# Delete a schedule route
@app.route('/schedule/delete')
def delete_schedule():
    iid = request.args.get('i_id')
    fid = request.args.get('f_id')
    data = airdb.delete_schedule(iid, fid)

    return data
# ---------------------------------------------------------
# SERVE THE APP
# ---------------------------------------------------------

if __name__ == '__main__':
    print('Connecting to db...{}'.format(config.dbname))

    app.run()
