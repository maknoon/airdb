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
        get_itineraries = json.loads(airdb.get_itinerary(1))
        return render_template('main.html', type='user', data=get_itineraries)
    elif session.get('type') == 'admin':
        return render_template('main.html', type='admin')
    else:
        return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    if (request.form['password'] == config.adminpwd
        and request.form['username'] == 'admin'):
        session['type'] = 'admin'
        return mainmenu()
    elif (request.form['password'] == config.userpwd
        and request.form['username'] == 'user'):
        session['type'] = 'user'
        return index()
    else:
        flash('wrong password!')

@app.route('/logout')
def logout():
    session['type'] = 'none'

    return index()


# ---------------------------------------------------------
# UI ENDPOINTS
# ---------------------------------------------------------
@app.route('/main', methods = ['POST'])
def mainmenu():
    return render_template('main.html', type='admin')

@app.route('/flightUI',methods = ['POST', 'GET'])
def flight():
   if request.method == 'POST':
      get_flights = json.loads(airdb.get_flight(None))
      return render_template('db.html', type = 'admin', tab = 'flight', data = get_flights)

@app.route('/airportUI',methods = ['POST', 'GET'])
def airport():
    if request.method == 'POST':
      get_airports = json.loads(airdb.get_airport(None))
      return render_template('db.html', type = 'admin', tab = 'airport', data = get_airports)

@app.route('/workscheduleUI', methods=['GET', 'POST', 'DELETE'])
def workschedule():
    get_work_schedule = json.loads(airdb.get_workson())

    if request.method == 'GET':
        employee_id = request.args.get('e_id')
        flight_id = request.args.get('f_id')
        filter_emp = request.args.get('filteremp')
        filter_flight = request.args.get('filterflight')
        should_delete = request.args.get('delete')
        if filter_emp is not None:
            get_work_schedule = json.loads(airdb.get_flight_for_employee(employee_id))
        elif filter_flight is not None:
            get_work_schedule = json.loads(airdb.get_employee_for_flight(flight_id))
        if should_delete is not None:
            airdb.delete_workson(employee_id, flight_id)
            get_work_schedule = json.loads(airdb.get_workson())

    elif request.method == 'POST':
        employee_id = request.form['e_id']
        flight_id = request.form['f_id']
        airdb.add_workson(employee_id, flight_id)
        get_work_schedule = json.loads(airdb.get_workson())

    return render_template('db.html', type ='admin', tab ='workschedule', data=get_work_schedule)

@app.route('/employeeUI', methods=['POST', 'GET', 'DELETE'])
def employee():
    get_employees = json.loads(airdb.get_employee(None))
    if request.method=='GET':
        employee_id = request.args.get('e_id')
        should_delete = request.args.get('delete')
        if should_delete is not None:
            airdb.delete_employee(employee_id)
            get_employees = json.loads(airdb.get_employee(None))
    elif request.method == 'POST':
        type = request.form['type']
        wage = request.form['wage']
        airdb.add_employee(0, type, wage)
        get_employees = json.loads(airdb.get_employee(None))

    return render_template('db.html', type = 'admin',  tab = 'employee', data = get_employees)

@app.route('/baggageUI',methods = ['POST', 'GET'])
def baggage():
    if request.method == 'POST':
      get_bags = json.loads(airdb.get_baggage(None))
      return render_template('db.html', type = 'admin',  tab = 'baggage', data = get_bags)

@app.route('/aircraftUI',methods = ['POST', 'GET'])
def aircraft():
    get_airplanes = json.loads(airdb.get_aircraft(None))
    if request.method =='GET':
        airport_id = request.args.get('airport_id')
        status = request.args.get('status')
        should_delete = request.args.get('delete')
        if status is not None:
            get_airplanes = json.loads(airdb.get_aircraft_by_status(status))
        elif airport_id is not None:
            get_airplanes = json.loads(airdb.get_aircraft_by_airport(airport_id))
    #elif request.method == 'POST':
    return render_template('db.html', type = 'admin', tab = 'aircraft', data = get_airplanes)

@app.route('/customerUI',methods = ['POST', 'GET'])
def customer():
    if request.method == 'POST':
      get_schedule = json.loads(airdb.get_schedule_for_itinerary(None))
      return render_template('db.html', type = 'admin',  tab = 'customer', data = get_schedule)

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
    flight_id = request.args.get('f_id')

    # fetch a customer by id
    if request.method == 'GET':
        if flight_id and cust_id is None: res_body = airdb.get_customer_for_flight(flight_id)
        else: res_body = airdb.get_customer(cust_id)
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
    i_id = request.args.get('id')
    # fetch bag by itinerary id
    if request.method == 'GET':
        res_body = airdb.get_baggage(i_id)
        if res_body == 0: abort(404)
    # add a new bag
    elif request.method == 'POST':
	    res_body = airdb.add_baggage(i_id, request.args.get('weight'))

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
    # Get total distance on trip if given itinerary id; itinerary if customer id
    elif request.method == 'GET':
        if i_id:
            res_body = get_itinerary_distance(i_id)
        else:
            cust_id = request.args.get('c_id')
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
        ap_id = request.args.get('ap_id')
        dept_or_arrv = request.args.get('dept_or_arrv')
        day = request.args.get('day')
        delayed = request.args.get('delayed')
        if ap_id and dept_or_arrv:
            res_body = airdb.get_flight_for_airport(ap_id, dept_or_arrv)
        elif day and dept_or_arrv:
            res_body = airdb.get_flight_for_day(day, dept_or_arrv)
        elif delayed:
            res_body = airdb.get_flight_delayed()
        else:
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

# =========
# /AIRCRAFT
# =========
@app.route('/aircraft', methods=['POST', 'GET', 'PATCH', 'DELETE'])
def aircraft_route():
    ac_id = request.args.get('id')

    # add a new aircraft
    if request.method == 'POST':
        req_body = request.get_json()
        res_body = airdb.add_aircraft(req_body['status'],  req_body['make'],
                 req_body['mileage'], req_body['datecreated'],
                 req_body['lastmaintained'], req_body['economy'],
                 req_body['business'], req_body['firstclass'],
                 req_body['airportid'])

    # fetch an aircraft by aircraft id
    elif request.method == 'GET':
        ap_id = request.args.get('ap_id')
        get_total = request.args.get('get_total')
        get_sorted_by_last_maintained = request.args.get('get_sorted_by_last_maintained')
        if ap_id and get_total:
            res_body = airdb.get_aircraft_by_airport_total(ap_id)
        elif get_sorted_by_last_maintained:
            res_body = airdb.get_aircraft_last_maintained()
        else:
            res_body = airdb.get_aircraft(ac_id)
        if res_body == 0: abort(404)

    # update an aircraft's status
    elif request.method == 'PATCH':
        req_body = request.get_json()
        aircraft = airdb.get_aircraft(ac_id)

        if aircraft == 0: abort(404)
        elif 'status' in req_body:
            res_body = airdb.update_aircraft(ac_id, 'AC_STATUS', wrapper(req_body['status']))

    # delete an aircraft
    elif request.method == 'DELETE':
        res_body = airdb.delete_aircraft(ac_id)

    return res_body

# =========
# /EMPLOYEE
# =========
@app.route('/employee', methods=['POST', 'DELETE'])
def employee_route():
    e_id = request.args.get('id')

    # add a new employee
    if request.method == 'POST':
        req_body = request.get_json()
        res_body = airdb.add_employee(req_body['hours'],  req_body['type'],
                 req_body['wage'])

    # delete an employee
    elif request.method == 'DELETE':
        res_body = airdb.delete_employee(e_id)

    return res_body

# =========
# /WORKSON
# =========
@app.route('/workson', methods=['POST', 'GET', 'DELETE'])
def workson_route():
    e_id = request.args.get('e_id')
    f_id = request.args.get('f_id')

    # add a new workson relation
    if request.method == 'POST':
        req_body = request.get_json()
        res_body = airdb.add_workson(req_body['e_id'], req_body['f_id'])

    # get employees with flight_id or flights with employee_id
    elif request.method == 'GET':
        if f_id and e_id is None:
            res_body = airdb.get_employee_for_flight(f_id)
        elif e_id and f_id is None:
            res_body = airdb.get_flight_for_employee(e_id)
        elif e_id is None and f_id is None: res_body = airdb.get_workson()
        if res_body == 0: abort(404)

    # delete a workson relations
    elif request.method == 'DELETE':
        res_body = airdb.delete_workson(e_id, f_id)

    return res_body

# ---------------------------------------------------------
# SERVE THE APP
# ---------------------------------------------------------

if __name__ == '__main__':
    print('Connecting to db...{}'.format(config.dbname))

    app.run()
