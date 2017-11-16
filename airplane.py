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
        get_airports = json.loads(airdb.get_airport(None))
        return render_template('db.html', type='admin', data=get_airports)

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

# Test add baggage
@app.route('/baggage')
def baggage_route():
    data = airdb.add_baggage(request.args.get('id'),
        request.args.get('weight'))

    return data

# Handle frequent fliers
@app.route('/ff', methods=['POST']) #, 'PATCH'])
def ff_route():
    ff_id = request.args.get('id')

    if (request.method == 'POST'):
        res_body = airdb.add_frequent_flier(ff_id)
    # elif (request.method == 'PATCH'):
    #     miles = request.get_json()['miles']
    #     res_body = airdb.update_frequent_flier(ff_id, miles)

    return res_body

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

# Handle gate endpoint
@app.route('/gate', methods=['GET', 'DELETE'])
def gate_route():
    apid = request.args.get('ap_id')
    gid = request.arg.get('g_id')

    # Get gates of airport by airport id
    if request.method == 'GET':
        res_body = airdb.get_gates_of_airport(apid)

    # Delete gate from airport
    elif request.method == 'DELETE':
        res_body = airdb.delete_gate(apid, gid)

    return res_body

# Handle schedule endpoint
@app.route('/schedule', methods=['GET', 'POST', 'DELETE'])
def schedule_route():
    iid = request.args.get('i_id')
    fid = request.args.get('f_id')

    # Get schedule of itinerary
    if request.method == 'GET':
        res_body = airdb.get_schedule_for_itinerary(iid)

    # Add schedule for itinerary
    elif request.method == 'POST':
        res_body.add_schedule(iid, fid)

    # Delete schedule by itinerary
    elif request.method == 'DELETE':
        res_body = airdb.delete_schedule(iid, fid)

    return res_body


# ---------------------------------------------------------
# SERVE THE APP
# ---------------------------------------------------------

if __name__ == '__main__':
    print('Connecting to db...{}'.format(config.dbname))

    app.run()
