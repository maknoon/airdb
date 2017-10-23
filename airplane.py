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

    return 'DB HAS BEEN RESET'


if __name__ == '__main__':
	print('Connecting to db...{}'.format(config.dbname))

	app.run()
