#!~/usr/bin/python
import MySQLdb
from datetime import datetime


class AirplaneDb(object):

    def __init__(self,host='',user='',pw='',db=''):
        self.host = host
        self.user = user
        self.pw = pw
        self.db = db


    '''
    EXAMPLE
    function: reset_db
    description: delete all tables in airdb and recreate
    notes: need to do in this order bc the tables are key-dependent
    '''
    def reset_db(self):
        airdb = MySQLdb.connect(host=self.host,
                                user=self.user,
                                passwd=self.pw,
                                db=self.db)
        cursor = airdb.cursor()

        drop = 'DROP TABLE IF EXISTS {}'
        cursor.execute(drop.format('USERS'))

        raw_users_query = """CREATE TABLE USERS (
                             U_ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                             U_NAME VARCHAR(32),
                             U_AGE INT,
                             U_HOME_ADDR VARCHAR(128),
                             U_PHONE_NUMBER VARCHAR(32) )"""
        cursor.execute(raw_users_query)
        print(('Created new {0} table in {1}').format('USERS',self.db))

        airdb.close()


