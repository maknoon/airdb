#!~/usr/bin/python
from flask import Flask, flash, abort, request, render_template, session
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
        return render_template('main.html', type='user')
    elif session.get('type') == 'admin':
        return render_template('main.html', type='admin')
    elif session.get('type') == 'employee':
        return employeeUI(1)
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
    elif (request.form['password'] == config.employeepwd
        and request.form['username'] == 'employee'):
        session['type'] = 'employee'
    else:
        session['type'] = 'none'
        flash('Invalid input')
        return render_template('index.html')

    return index()

@app.route('/logout')
def logout():
    session['type'] = 'none'

    return index()

# ---------------------------------------------------------
# USER UI
# ---------------------------------------------------------
@app.route('/mainuser', methods = ['POST'])
def mainmenuuser():
    return render_template('main.html', type ='user')

@app.route('/user-account-view', methods = ['POST', 'GET'])
def useraccountUI():
    get_customer = json.loads(airdb.get_customer(1))
    get_ff = json.loads(airdb.get_frequent_flier(1))
    if request.method == 'POST':
        if 'updateemail' in request.form:
            if request.form['email'] == '': res = 500
            else:
                newemail = '"{}"'.format(request.form['email'])
                res = airdb.update_customer(1, 'C_EMAIL', newemail)
        elif 'updatephone' in request.form:
            if request.form['phone'] == '': res = 500
            else:
                newphone = '"{}"'.format(request.form['phone'])
                res = airdb.update_customer(1, 'C_PHONE', newphone)

        flash(res)
        get_customer = json.loads(airdb.get_customer(1))
    return render_template('alerts.html', type='user', tab='account',
        data1=get_customer, data2=get_ff, alert_t='update')

@app.route('/user-itinerary-view', methods = ['POST', 'GET'])
def useritineraryUI():
    get_itineraries = json.loads(airdb.get_itinerary_with_distance(1))
    get_old = json.loads(airdb.get_old_itinerary(1))
    alert_t = 'update'

    if request.method == 'POST':
        itinerary_id = request.form['i_id']
        if itinerary_id == '': flash(500)
        else:
            if 'updatestatus' in request.form:
                if airdb.update_itinerary(itinerary_id, 'I_STATUS', '"CHECKEDIN"') == 1:
                    alert_t = 'user_error'
                flash(200)
            elif 'updateseat' in request.form:
                seattype = '"{}"'.format(request.form['seat'])
                if airdb.update_itinerary(itinerary_id, 'I_SEATTYPE', seattype) == 1:
                    alert_t = 'user_error'
                flash(200)
            elif 'delete' in request.form:
                alert_t = 'delete'
                if airdb.delete_itinerary(itinerary_id) == 1:
                    alert_t = 'user_error'
                flash(200)
            get_itineraries = json.loads(airdb.get_itinerary_with_distance(1))

            return render_template('alerts.html', type='user', tab='itinerary',
                data=get_itineraries, data2=get_old, alert_t=alert_t)

    return render_template('db.html', type='user', tab='itinerary',
        data=get_itineraries, data2=get_old)

@app.route('/user-specific-view', methods=['POST', 'GET'])
def userspecificUI():
    alert_t = 'insert'
    if request.method == 'POST':
        itinerary_id = request.form['i_id']
        if itinerary_id == '': flash(500)
        else:
            if 'addbaggage' in request.form:
                if request.form['b_weight'] == '': flash(500)
                else:
                    if airdb.add_baggage(itinerary_id, request.form['b_weight']) == 0: flash(500)
                    else: flash(200)
            elif 'removebaggage' in request.form:
                if request.form['b_id'] == '': flash(500)
                else:
                    alert_t = 'delete'
                    if airdb.delete_baggage(request.form['b_id']) == 0: flash(500)
                    else: flash(200)
            get_itinerary = json.loads(airdb.get_customer_itinerary_info(itinerary_id))
            get_bags = json.loads(airdb.get_baggage(itinerary_id))

            return render_template('alerts.html', type='user', tab='specific',
                data1=get_itinerary, data2=get_bags, alert_t=alert_t)

    return render_template('alerts.html', type='user', tab='specific', alert_t=alert_t)

# ---------------------------------------------------------
# EMPLOYEE UI
# ---------------------------------------------------------
@app.route('/employee-view', methods=['POST'])
def employeeUI(id):
    get_employee = json.loads(airdb.get_employee(id))
    get_schedule = json.loads(airdb.get_schedule_for_employee(id))
    get_vip = json.loads(airdb.get_vip())
    return render_template('db.html', type='employee', data1 = get_employee, data2 = get_schedule, data3 = get_vip)

# ---------------------------------------------------------
# ADMIN UI
# ---------------------------------------------------------
@app.route('/main', methods = ['POST'])
def mainmenu():
    return render_template('main.html', type='admin')

@app.route('/admin-airport-view',methods = ['GET'])
def airport():
    get_airports = json.loads(airdb.get_aircraft_by_airport_total())
    return render_template('db.html', type='admin', tab='airport', data=get_airports)

@app.route('/admin-aircraft-view',methods = ['POST', 'GET'])
def aircraft():
    get_airplanes = json.loads(airdb.get_aircraft(None))

    if request.method =='POST':
        alert_t = 'update'
        if 'filterairport' in request.form:
            if request.form['airport_id'] == '': flash(500)
            else:
                get_airplanes = json.loads(airdb.get_aircraft_by_airport(request.form['airport_id']))
                if get_airplanes == 0: flash(500)
        elif 'filterstatus' in request.form:
            if request.form['status'] == '': flash(500)
            else:
                get_airplanes = json.loads(airdb.get_aircraft_by_status(request.form['status']))
                if get_airplanes == 0: flash(500)
        elif 'updatestatus' in request.form:
            if request.form['ac_id'] == '' or request.form['status'] == '': flash(500)
            else:
                status = '"{}"'.format(request.form['status'])
                if airdb.update_aircraft(request.form['ac_id'], status) == 0: flash(500)
                else:
                    flash(200)
                    get_airplanes = json.loads(airdb.get_aircraft(request.form['ac_id']))
        return render_template('alerts.html', type='admin', tab='aircraft',
            data=get_airplanes, alert_t=alert_t)

    return render_template('db.html', type='admin', tab='aircraft', data=get_airplanes)

@app.route('/admin-flight-view',methods = ['POST', 'GET'])
def flight():
    get_flights = json.loads(airdb.get_flight(None))
    original = get_flights
    if request.method == 'GET':
        delayed = request.args.get('delayed')
        if delayed == 'True':
            get_flights = json.loads(airdb.get_delayed_flight())
        else:
            get_flights = json.loads(airdb.get_flight(None))

    elif request.method =='POST':
        alert_t = 'update'
        if 'filterarriving' in request.form:
            if request.form['ap_id'] == '': flash(500)
            else: get_flights = json.loads(airdb.get_flight_for_airport(request.form['ap_id'], 'arrv'))
        elif 'filterdeparting' in request.form:
            if request.form['ap_id'] == '': flash(500)
            else: get_flights = json.loads(airdb.get_flight_for_airport(request.form['ap_id'], 'dept'))
        elif 'updatestatus' in request.form:
            if request.form['f_id'] == '' or request.form['status'] == '': flash(500)
            else:
                status = '"{}"'.format(request.form['status'])
                if airdb.update_flight(request.form['f_id'], 'F_STATUS', status) == 0: flash(500)
                else:
                    flash(200)
                    get_flights = json.loads(airdb.get_flight(None))
        if get_flights == '':
            flash(500)
            get_flights = original
        return render_template('alerts.html', type='admin', tab='flight', data=get_flights, alert_t=alert_t)

    return render_template('db.html', type='admin', tab='flight', data=get_flights)

@app.route('/admin-baggage-view',methods = ['POST', 'GET'])
def baggage():
    get_bags = json.loads(airdb.get_baggage(None))

    if request.method == 'POST':
        alert_t = 'insert'
        if 'filteritinerary' in request.form:
            if request.form['i_id'] == '': flash(500)
            else:
                get_bags = json.loads(airdb.get_baggage(request.form['i_id']))
                if get_bags == 0: flash(500)
        elif 'filterflight' in request.form:
            if request.form['f_id'] == '': flash(500)
            else:
                get_bags = json.loads(airdb.get_baggage_for_flight(request.form['f_id']))
                if get_bags == 0: flash(500)
        return render_template('alerts.html', type='admin', tab='baggage',
            data=get_bags, alert_t=alert_t)

    return render_template('db.html', type='admin', tab='baggage', data=get_bags)

@app.route('/admin-work-schedule-view', methods=['GET', 'POST'])
def workschedule():
    get_work_schedule = json.loads(airdb.get_workson())

    if request.method == 'POST':
        alert_t = 'insert'
        if 'filteremp' in request.form:
            if request.form['e_id'] == '': flash(500)
            else: get_work_schedule = json.loads(airdb.get_flight_for_employee(request.form['e_id']))
        elif 'filterflight' in request.form:
            if request.form['f_id'] == '': flash(500)
            else: get_work_schedule = json.loads(airdb.get_employee_for_flight(request.form['f_id']))
        elif 'add' in request.form:
            if request.form['e_id'] == '' or request.form['f_id'] == '': flash(500)
            elif airdb.add_workson(request.form['e_id'], request.form['f_id']) == 0: flash(500)
            else: flash(200)
            get_work_schedule = json.loads(airdb.get_workson())
        elif 'delete' in request.form:
            alert_t = 'delete'
            if request.form['e_id'] == '' or request.form['f_id'] == '': flash(500)
            elif airdb.delete_workson(request.form['e_id'], request.form['f_id']) == 0: flash(500)
            else: flash(200)
            get_work_schedule = json.loads(airdb.get_workson())
        return render_template('alerts.html', type='admin', tab='workschedule',
            data=get_work_schedule, alert_t=alert_t)

    return render_template('db.html', type='admin', tab='workschedule', data=get_work_schedule)

@app.route('/admin-employee-view', methods=['GET', 'POST'])
def employee():
    if request.method == 'GET':
        get_employees = json.loads(airdb.get_employee(None))

    elif request.method == 'POST':
        alert_t = 'insert'
        if 'add' in request.form:
            employee_type = request.form['type']
            employee_name = request.form['name']
            wage = request.form['wage']
            if employee_name == '' or employee_type == '' or wage == '': flash(500)
            elif airdb.add_employee(0, employee_type, employee_name, wage) == 0: flash(500)
            else: flash(200)
        elif 'delete' in request.form:
            alert_t = 'delete'
            employee_to_delete = request.form['e_id']
            if employee_to_delete == '': flash(500)
            elif airdb.delete_employee(employee_to_delete) == 0: flash(500)
            else: flash(200)
        get_employees = json.loads(airdb.get_employee(None))

        return render_template('alerts.html', type='admin', tab='employee',
            data=get_employees, alert_t=alert_t)

    return render_template('db.html', type='admin', tab='employee', data=get_employees)

@app.route('/admin-customer-view',methods = ['POST', 'GET'])
def customer():
    if request.method == 'GET':
        flight_id = request.args.get('f_id')
        customer_id = request.args.get('c_id')
        filter_customer= request.args.get('filtercustomer')
        filter_flight = request.args.get('filterflight')
        if filter_flight is not None and flight_id is not None and flight_id != '':
            get_schedule = json.loads(airdb.get_schedule_for_itinerary(None, None, flight_id))
        elif filter_customer is not None and customer_id is not None and customer_id != '':
            get_schedule = json.loads(airdb.get_schedule_for_itinerary(None, customer_id, None))
        else:
            get_schedule = json.loads(airdb.get_schedule_for_itinerary(None, None, None))
    elif request.method =='POST':
        customer_id = request.form['c_id']
        status = '"{}"'.format('CHECKEDIN')
        airdb.update_itinerary(customer_id, 'I_STATUS', status)
        get_schedule = json.loads(airdb.get_schedule_for_itinerary(None, None, None))
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
        res_body = airdb.get_schedule_for_itinerary(iid, None, None)

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
        res_body = airdb.add_employee(req_body['hours'],  req_body['type'], req_body['name'],
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

# =========
# /VIP
# =========
@app.route('/vip', methods=['GET'])
def vip_route():
    # get all VIPS (customer that flied/flies firstclass)
    if request.method == 'GET':
        res_body = airdb.get_vip()
        if res_body == 0: abort(404)
    else:
        abort(400)
    return res_body

# ---------------------------------------------------------
# SERVE THE APP
# ---------------------------------------------------------

if __name__ == '__main__':
    print('Connecting to db...{}'.format(config.dbname))

    app.run()
