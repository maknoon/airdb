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
        # get all itineraries
        get_itineraries = json.loads(airdb.get_itinerary(1))

        return render_template('db.html', type='user', data=get_itineraries)
    elif session.get('type') == 'admin':
        # get all airports
        get_airports = json.loads(airdb.get_airport(None))

        return render_template('db.html', type='admin', data=get_airports)
    else:

        return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if (request.form['password'] == config.adminpwd
        and request.form['username'] == 'admin'):
        session['type'] = 'admin'
    elif (request.form['password'] == config.userpwd
        and request.form['username'] == 'user'):
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

# Helper
def wrapper(str_db_value):
    return '"{}"'.format(str_db_value)

# =========
# /CUSTOMER
# =========
@app.route('/customer', methods=['POST','PATCH','GET'])
def customer_route():
    cust_id = request.args.get('id')

    # fetch a customer by id
    if request.method == 'GET':
        res_body = airdb.get_customer(cust_id)
        if res_body == 0: abort(404)

    # add a new customer
    elif request.method == 'POST':
        req_body = request.get_json()
        cust_name = req_body['name']
        res_body = airdb.add_customer(cust_name, req_body['age'], req_body['email'],
            req_body['phone'])

    # update a customer
    elif request.method == 'PATCH':
        req_body = request.get_json()
        customer = airdb.get_customer(cust_id)

        if customer == 0: abort(404)
        else:
            if 'phone' in req_body:
                airdb.update_customer(cust_id, 'C_PHONE', wrapper(req_body['phone']))
            if 'email' in req_body:
                airdb.update_customer(cust_id, 'C_EMAIL', wrapper(req_body['email']))
            if 'age' in req_body:
                airdb.update_customer(cust_id, 'C_AGE', req_body['age'])
            if 'name' in req_body:
                airdb.update_customer(cust_id, 'C_NAME', wrapper(req_body['name']))

            res_body = airdb.get_customer(cust_id)

    return res_body

# =========
# /BAGGAGE
# =========
@app.route('/baggage', methods=['POST', 'GET'])
def baggage_route():
    c_id = request.args.get('id')
    # fetch bag by customer id
    if request.method == 'GET':
        res_body = airdb.get_baggage(c_id)
        if res_body == 0: abort(404)
	# add a new bag
    elif request.method == 'POST':
	    res_body = airdb.add_baggage(c_id, request.args.get('weight'))
    return res_body
# =========
# /FF
# =========
@app.route('/ff', methods=['POST', 'PATCH'])
def ff_route():
    ff_id = request.args.get('id')

    if (request.method == 'POST'):
        res_body = airdb.add_frequent_flier(ff_id)
    elif (request.method == 'PATCH'):
        m = request.args.get('miles')
        res_body = airdb.update_frequent_flier(ff_id, m)
    return res_body

# =========
# /ITINERARY
# =========
@app.route('/itinerary', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def itinerary_route():
    i_id = request.args.get('id')

    if request.method == 'POST':
        req_body = request.get_json()
        res_body = airdb.add_itinerary(req_body['seattype'],
                                        req_body['seatcost'],
                                        req_body['status'],
                                        req_body['customer_id'])

    elif request.method == 'GET':
        cust_id = request.args.get('id')
        res_body = airdb.get_itinerary(cust_id)
        if res_body == 0: abort(404)

    elif request.method == 'PATCH':
        req_body = request.get_json()
        if 'seatcost' in req_body:
            res_body = airdb.update_itinerary(i_id, 'I_SEATCOST', float(req_body['seatcost']))
        if 'seattype' in req_body:
            res_body = airdb.update_itinerary(i_id, 'I_SEATTYPE', wrapper(req_body['seattype']))
        if 'status' in req_body:
            res_body = airdb.update_itinerary(i_id, 'I_STATUS', wrapper(req_body['status']))

    elif request.method == 'DELETE':
        res_body = airdb.delete_itinerary(i_id)

    return res_body

# =========
# /FLIGHT
# =========
@app.route('/flight', methods=['GET','POST', 'PATCH'])
def flight_route():
    if request.method == 'POST':
        req_body = request.get_json()
        res_body = airdb.add_flight(req_body['aircraft'],
                                    req_body['distance'],
                                    req_body['departtime'],
                                    req_body['atime'],
                                    req_body['dairport'],
                                    req_body['aairport'],
                                    req_body['dgate'],
                                    req_body['agate'],
                                    req_body['status'])
    elif request.method == 'PATCH':
        f_id = request.args.get('id')
        req_body = request.get_json()
        if 'aircraft' in req_body:
            res_body = airdb.update_flight(f_id, 'AC_ID', req_body['aircraft'])
        if 'distance' in req_body:
            res_body = airdb.update_flight(f_id, 'F_DISTANCE', float(req_body['distance']))
        if 'departtime' in req_body:
            res_body = airdb.update_flight(f_id, 'F_DEPARTURETIME', wrapper(req_body['departtime']))
        if 'arrivetime' in req_body:
            res_body = airdb.update_flight(f_id, 'F_ARRIVALTIME', wrapper(req_body['arrivetime']))
        if 'departairport' in req_body:
            res_body = airdb.update_flight(f_id, 'F_DEPARTUREAIRPORTID', wrapper(req_body['departairport']))
        if 'arriveairport' in req_body:
            res_body = airdb.update_flight(f_id, 'F_ARRIVALAIRPORTID', wrapper(req_body['arriveairport']))
        if 'departgate' in req_body:
            res_body = airdb.update_flight(f_id, 'F_DEPARTUREGATEID', wrapper(req_body['departgate']))
        if 'arrivegate' in req_body:
            res_body = airdb.update_flight(f_id, 'F_ARRIVALGATEID', wrapper(req_body['arrivegate']))
        if 'status' in req_body:
            res_body = airdb.update_flight(f_id, 'F_STATUS', wrapper(req_body['status']))
    elif request.method == 'GET':
        f_id = request.args.get('id')
        res_body = airdb.get_flight(f_id)
        if res_body == 0: abort(404)
    return res_body

# =========
# /AIRPORT
# =========
@app.route('/airport', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def airport_route():
    apid = request.args.get('id')

    # fetch a airport by id
    if request.method == 'GET':
        res_body = airdb.get_airport(apid)
        if res_body == 0: abort(404)

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
                airdb.update_airport(apid, 'AP_COUNTRY', wrapper(req_body['country']))
            if 'city' in req_body:
                airdb.update_airport(apid, 'AP_CITY', wrapper(req_body['city']))
            airport = airdb.get_airport(apid)
            airport_json = {'airport_id':apid,'city':airport[1],
                            'country':airport[2]}
            res_body = json.dumps(airport_json, indent=4, separators=(',', ': '))

    # delete an airport
    elif request.method == 'DELETE':
        res_body = airdb.delete_airport(apid)

    return res_body

# =========
# /GATE
# =========
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

# =========
# /SCHEDULE
# =========
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
