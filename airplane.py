#!~/usr/bin/python
from flask import Flask, flash, request, render_template, session
from airplanedb import AirplaneDb
import config
import hashlib

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

# test get new customer
@app.route('/customer')
def get_customer():
    cust_id = request.args.get('id')
    data = airdb.get_customer(cust_id)

    return data

# test create new customer
@app.route('/customer/new')
def add_customer():
    cust_name = request.args.get('name')
    data = airdb.add_customer(cust_name,
        request.args.get('age'), request.args.get('email'),
        request.args.get('phone'))

    return data


# test update customer
# @app.route('/customer/update')
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

# update frequent flier miles route
@app.route('/ff/update')
def update_frequent_flier():
    cust_id = request.args.get('id')
    miles = request.args.get('miles')
    data = airdb.update_frequent_flier(cust_id, miles)

    return data

# test add itinerary
@app.route('/itinerary/new')
def add_itinerary():
    cust_id = request.args.get('id')
    data = airdb.add_itinerary(request.args.get('seattype'),
                                request.args.get('seatcost'),
                                request.args.get('status'), cust_id)

    return data

# test delete itinerary
@app.route('/itinerary/delete')
def delete_itinerary():
    id = request.args.get('i_id')
    data = airdb.delete_itinerary(id)

    return data

# test update itinerary
@app.route('/itinerary/update')
def update_itinerary():
    i_id = request.args.get('id')
    new_value = request.args.get('new')
    itinerary_field = request.args.get('field')
    data = airdb.update_itinerary(i_id, itinerary_field, new_value)

    return data

# test add flight
@app.route('/flight/new')
def add_flight():
    data = airdb.add_flight(request.args.get('aircraft'),
                             request.args.get('distance'),
                             request.args.get('dtime'),
                             request.args.get('atime'),
                             request.args.get('dairport'),
                             request.args.get('aairport'),
                             request.args.get('dgate'),
                             request.args.get('agate'),
                             request.args.get('status'))

    return data

# test update flight
@app.route('/flight/update')
def update_flight():
    f_id = request.args.get('id')
    new_value = request.args.get('new')
    flight_field=request.args.get('field')
    data = airdb.update_flight(f_id, flight_field, new_value)

    return data

# Add airport route
@app.route('/airport/new')
def add_airport():
    data = airdb.add_airport(request.args.get('id'),
        request.args.get('city'), request.args.get('country'))

    return data

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


# Delete a gate route
@app.route('/gate/delete')
def delete_gate():
    apid = request.args.get('ap_id')
    gid = request.args.get('g_id')
    data = airdb.delete_gate(apid, gid)

    return data

# Add new aircraft to table AIRCRAFT
@app.route('/aircraft/new')
def add_aircraft():
	data = airdb.add_aircraft(request.args.get('status'), request.args.get('make'),
		request.args.get('mileage'), request.args.get('datecreated'),
		request.args.get('lastmaintained'), request.args.get('economy'),
	 	request.args.get('business'), request.args.get('firstclass'),
	 	request.args.get('airportid'))

	return data

# Get aircrafts with specified aircraft_id in table AIRCRAFT
@app.route('/aircraft/get')
def get_aircraft():
	data = airdb.get_aircraft(request.args.get('id'))

	return data

# Update aircraft's status in table AIRCRAFT
@app.route('/aircraft/update')
def update_aircraft():
	data = airdb.update_aircraft(request.args.get('id'),request.args.get('status'),
		request.args.get('newstatus'))

	return data

# Delete aircraft in table AIRCRAFT
@app.route('/aircraft/delete')
def delete_aircraft():
	data = airdb.delete_aircraft(request.args.get('id'))

	return data

# Add new employee to table EMPLOYEE
@app.route('/employee/new')
def add_employee():
    data = airdb.add_employee(request.args.get('hours'), request.args.get('type'),
        request.args.get('wage'))

    return data

# Get employees with specified flight_ID in table WORKSON
@app.route('/flight/getemployeeforflight')
def get_employee_for_flight():
	data = airdb.get_employee_for_flight(request.args.get('f_id'))

	return data

# Get flights with specified employee_ID in table Workson
@app.route('/employee/getflightforemployee')
def get_flight_for_employee():
	data = airdb.get_flight_for_employee(request.args.get('e_id'))

	return data

# Delete employee in table EMPLOYEE
@app.route('/employee/delete')
def delete_employee():
	data = airdb.delete_employee(request.args.get('id'))

	return data

# Get schedule of ITINERARY
@app.route('/schedule/getForItinerary')
def get_schedule_for_itinerary():
    iid = request.args.get('id')
    data = airdb.get_schedule_for_itinerary(iid)

    return data

# Add a new workson relation to table WORKSON
@app.route('/workson/new')
def add_workson():
    data = airdb.add_workson(request.args.get('e_id'), request.args.get('f_id'))

    return data

# Delete a workson relation in table Workson
@app.route('/workson/delete')
def delete_workson():
    data = airdb.delete_workson(request.args.get('e_id'), request.args.get('f_id'))

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
