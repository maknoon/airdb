#!~/usr/bin/python
import MySQLdb
from datetime import datetime


class AirplaneDb(object):

    def __init__(self,host='',user='',pw='',db=''):
        self.host = host
        self.user = user
        self.pw = pw
        self.db = db

        self.airdb = MySQLdb.connect(host=self.host,
                                     user=self.user,
                                     passwd=self.pw,
                                     db=self.db)

    '''
    EXAMPLE
    function: reset_db
    description: delete all tables in airdb and recreate
    notes: need to do in this order bc the tables are key-dependent
    '''
    def reset_db(self):
        cursor = self.airdb.cursor()

        drop = 'DROP TABLE IF EXISTS {}'
        cursor.execute(drop.format('SCHEDULE'))
        cursor.execute(drop.format('WORKSON'))
        cursor.execute(drop.format('FREQUENTFLIER'))
        cursor.execute(drop.format('ITINERARY'))
        cursor.execute(drop.format('EMPLOYEE'))
        cursor.execute(drop.format('FLIGHT'))
        cursor.execute(drop.format('AIRCRAFT'))
        cursor.execute(drop.format('GATE'))
        cursor.execute(drop.format('AIRPORT'))
        cursor.execute(drop.format('BAGGAGE'))
        cursor.execute(drop.format('CUSTOMER'))

        create_customer_table = """CREATE TABLE CUSTOMER (
				                C_ID INT NOT NULL AUTO_INCREMENT,
                            	C_NAME VARCHAR(32) NOT NULL,
                            	C_AGE INT NOT NULL,
                            	C_EMAIL VARCHAR(128) NOT NULL,
                            	C_PHONE VARCHAR(32) NOT NULL,
	                            PRIMARY KEY (C_ID)
				                )"""

        create_baggage_table = """CREATE TABLE BAGGAGE (
                				B_ID INT NOT NULL,
                				C_ID INT NOT NULL,
                				B_WEIGHT DECIMAL(5,2) NOT NULL,
                				FOREIGN KEY (C_ID) REFERENCES CUSTOMER(C_ID),
                				PRIMARY KEY (B_ID)
                                )"""

        create_airport_table = """CREATE TABLE AIRPORT (
                				AP_ID VARCHAR(32) NOT NULL UNIQUE,
                				AP_CITY VARCHAR(32) NOT NULL,
                				AP_COUNTRY VARCHAR(32) NOT NULL,
                				PRIMARY KEY (AP_ID)
                				)"""

        create_gate_table = """CREATE TABLE GATE (
            				G_ID VARCHAR(32) NOT NULL,
            				AP_ID VARCHAR(32) NOT NULL,
            				FOREIGN KEY (AP_ID) REFERENCES AIRPORT(AP_ID),
            				PRIMARY KEY (AP_ID, G_ID)
            				)"""

        create_aircraft_table = """CREATE TABLE AIRCRAFT (
                                AC_ID VARCHAR(32) NOT NULL UNIQUE,
                                AC_STATUS VARCHAR(32) NOT NULL,
                                AC_MAKE VARCHAR(32) NOT NULL,
                                AC_MILEAGE FLOAT NOT NULL,
                                AC_DATE_CREATED VARCHAR(32) NOT NULL,
                                AC_LAST_MAINTAINED VARCHAR(32),
                                AC_NUM_ECONOMY INT NOT NULL,
                                AC_NUM_BUSINESS INT NOT NULL,
                                AC_NUM_FIRSTCLASS INT NOT NULL,
                                AP_ID VARCHAR(32),
                                PRIMARY KEY (AC_ID),
                                FOREIGN KEY (AP_ID) REFERENCES AIRPORT(AP_ID)
                                )"""
                                
        create_flight_table = """CREATE TABLE FLIGHT (
                                F_ID VARCHAR(32) NOT NULL UNIQUE,
                                AC_ID VARCHAR(32) NOT NULL,
                                F_DISTANCE FLOAT NOT NULL,
                                F_DEPARTURETIME VARCHAR(32) NOT NULL,
                                F_ARRIVALTIME VARCHAR(32) NOT NULL,
                                F_DEPARTUREAIRPORTID VARCHAR(32) NOT NULL,
                                F_ARRIVALAIRPORTID VARCHAR(32) NOT NULL,
                                F_DEPARTUREGATEID VARCHAR(32) NOT NULL,
                                F_ARRIVALGATEID VARCHAR(32) NOT NULL,
                                F_STATUS VARCHAR(32) NOT NULL,
                                PRIMARY KEY (F_ID),
                                CHECK (F_DEPARTUREAIRPORTID <> F_ARRIVALAIRPORTID),
                                FOREIGN KEY (AC_ID) REFERENCES AIRCRAFT(AC_ID),
                                FOREIGN KEY (F_DEPARTUREAIRPORTID, F_DEPARTUREGATEID) REFERENCES GATE(AP_ID, G_ID),
                                FOREIGN KEY (F_ARRIVALAIRPORTID, F_ARRIVALGATEID) REFERENCES GATE(AP_ID, G_ID)
                                )"""

        create_employee_table = """CREATE TABLE EMPLOYEE (
                                E_ID VARCHAR(32) NOT NULL UNIQUE,
                                E_HOURS FLOAT NOT NULL,
                                E_TYPE VARCHAR(32) NOT NULL,
                                E_WAGE FLOAT NOT NULL,
                                PRIMARY KEY (E_ID)
                                )"""

        create_itinerary_table = """CREATE TABLE ITINERARY (
                                I_ID VARCHAR(32) NOT NULL UNIQUE,
                                I_SEATTYPE VARCHAR(32) NOT NULL,
                                I_SEATCOST FLOAT NOT NULL,
                                I_STATUS VARCHAR(32) NOT NULL,
                                C_ID INT NOT NULL,
                                PRIMARY KEY (I_ID),
                                FOREIGN KEY (C_ID) REFERENCES CUSTOMER(C_ID)
                                )"""

        create_frequentflier_table = """CREATE TABLE FREQUENTFLIER (
                                    C_ID INT NOT NULL,
                                    FF_MILES FLOAT NOT NULL,
                                    PRIMARY KEY (C_ID),
                                    FOREIGN KEY (C_ID) REFERENCES CUSTOMER(C_ID)
                                    )"""

        create_workson_table = """CREATE TABLE WORKSON (
                                E_ID VARCHAR(32) NOT NULL,
                                F_ID VARCHAR(32) NOT NULL,
                                FOREIGN KEY (E_ID) REFERENCES EMPLOYEE(E_ID),
                                FOREIGN KEY (F_ID) REFERENCES FLIGHT(F_ID),
                                PRIMARY KEY (E_ID, F_ID)
                                )"""

        create_schedule_table = """CREATE TABLE SCHEDULE (
                                I_ID VARCHAR(32) NOT NULL,
                                F_ID VARCHAR(32) NOT NULL,
                                FOREIGN KEY (I_ID) REFERENCES ITINERARY(I_ID),
                                FOREIGN KEY (F_ID) REFERENCES FLIGHT(F_ID),
                                PRIMARY KEY (I_ID, F_ID)
                                )"""

    	cursor.execute(create_customer_table)
    	print(('Created new {0} table in {1}').format('CUSTOMER',self.db))

        cursor.execute(create_baggage_table)
        print(('Created new {0} table in {1}').format('BAGGAGE',self.db))

    	cursor.execute(create_airport_table)
    	print(('Created new {0} table in {1}').format('AIRPORT',self.db))

        cursor.execute(create_gate_table)
    	print(('Created new {0} table in {1}').format('GATE',self.db))

        cursor.execute(create_aircraft_table)
    	print(('Created new {0} table in {1}').format('AIRCRAFT',self.db))

        cursor.execute(create_flight_table)
    	print(('Created new {0} table in {1}').format('FLIGHT',self.db))

        cursor.execute(create_employee_table)
    	print(('Created new {0} table in {1}').format('EMPLOYEE',self.db))

        cursor.execute(create_itinerary_table)
    	print(('Created new {0} table in {1}').format('ITINERARY',self.db))

        cursor.execute(create_frequentflier_table)
    	print(('Created new {0} table in {1}').format('FREQUENTFLIER',self.db))

        cursor.execute(create_workson_table)
    	print(('Created new {0} table in {1}').format('WORKSON',self.db))

        cursor.execute(create_schedule_table)
    	print(('Created new {0} table in {1}').format('SCHEDULE',self.db))

        self.airdb.close()
