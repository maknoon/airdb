#!~/usr/bin/python
from flask import Flask, request
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
    airdb.add_baggage(request.args.get('id'), request.args.get('weight'))

    return 'ADDED BAGGAGE'


@app.route('/ffupdate')
def update_frequent_flier():
    cust_id = request.args.get('id')
    miles = request.args.get('miles')
    airdb.update_frequent_flier(cust_id, miles)  

    return 'ADDED %s MILES TO ACCOUNT' %(str(miles))


# test add itinerary
@app.route('/itinerary')
def add_itinerary():
    cust_id = request.args.get('id')
    added = airdb.add_itinerary(request.args.get('seattype'),
                                request.args.get('seatcost'),
                                request.args.get('status'), cust_id)

    return 'ADDED NEW ITINERARY %s FOR CUSTOMER %s' % (added, str(cust_id))


# test delete itinerary
@app.route('/itinerarydelete')
def delete_itinerary():
    id = request.args.get('i_id')
    airdb.delete_itinerary(id)

    return 'DELETED ITINERARY %s' % (id)


# test update itinerary
@app.route('/itineraryupdate')
def update_itinerary():
    id = request.args.get('i_id')
    new_value = request.args.get('new')
    itinerary_field = request.args.get('field')
    airdb.update_itinerary(id, itinerary_field, new_value)

    return 'Updated {0} in ITINERARY {1} to {2}'.format(itinerary_field, id, new_value)


# test add flight
@app.route('/flight')
def add_flight():
    added = airdb.add_flight(request.args.get('aircraft'),
                             request.args.get('distance'),
                             request.args.get('dtime'),
                             request.args.get('atime'),
                             request.args.get('dairport'),
                             request.args.get('aairport'),
                             request.args.get('dgate'),
                             request.args.get('agate'),
                             request.args.get('status'))

    return 'ADDED NEW FLIGHT {0}'.format(added)


# test update flight
@app.route('/flightupdate')
def update_flight():
    id = request.args.get('f_id')
    new_value = request.args.get('new')
    flight_field=request.args.get('field')
    airdb.update_flight(id, flight_field, new_value)

    return 'Updated {0} in FLIGHT {1} to {2}'.format(flight_field, id, new_value)


# ---------------------------------------------------------
# SERVE THE APP
# ---------------------------------------------------------

if __name__ == '__main__':
    print('Connecting to db...{}'.format(config.dbname))
    app.secret_key = os.urandom(12)
    
    app.run()

