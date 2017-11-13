#!~/usr/bin/python
from flask import Flask
from airplanedb import AirplaneDb
import config

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


if __name__ == '__main__':
    print('Connecting to db...{}'.format(config.dbname))

    app.run()
