#!~/usr/bin/python
import MySQLdb
from datetime import datetime
from flask import jsonify
import json


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
        db = MySQLdb.connect(host=self.host,
                                 user=self.user,
                                 passwd=self.pw,
                                 db=self.db)
        cursor = db.cursor()
        drop = 'DROP TABLE IF EXISTS {}'
        cursor.execute(drop.format('SCHEDULE'))
        cursor.execute(drop.format('WORKSON'))
        cursor.execute(drop.format('FREQUENTFLIER'))
        cursor.execute(drop.format('BAGGAGE'))
        cursor.execute(drop.format('ITINERARY'))
        cursor.execute(drop.format('EMPLOYEE'))
        cursor.execute(drop.format('FLIGHT'))
        cursor.execute(drop.format('AIRCRAFT'))
        cursor.execute(drop.format('GATE'))
        cursor.execute(drop.format('AIRPORT'))
        cursor.execute(drop.format('CUSTOMER'))

        create_customer_table = """CREATE TABLE CUSTOMER (
                                C_ID INT AUTO_INCREMENT,
                                C_NAME VARCHAR(32) NOT NULL,
                                C_AGE INT NOT NULL,
                                C_EMAIL VARCHAR(128) NOT NULL,
                                C_PHONE VARCHAR(32) NOT NULL,
                                PRIMARY KEY (C_ID)
                                )"""

        create_airport_table = """CREATE TABLE AIRPORT (
                                AP_ID VARCHAR(32),
                                AP_CITY VARCHAR(32) NOT NULL,
                                AP_COUNTRY VARCHAR(32) NOT NULL,
                                PRIMARY KEY (AP_ID)
                                )"""

        create_gate_table = """CREATE TABLE GATE (
                            G_ID VARCHAR(32),
                            AP_ID VARCHAR(32),
                            FOREIGN KEY (AP_ID) REFERENCES AIRPORT(AP_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                            PRIMARY KEY (AP_ID, G_ID)
                            )"""

        create_aircraft_table = """CREATE TABLE AIRCRAFT (
                                AC_ID INT AUTO_INCREMENT,
                                AC_STATUS VARCHAR(32) NOT NULL,
                                AC_MAKE VARCHAR(32) NOT NULL,
                                AC_MILEAGE FLOAT NOT NULL,
                                AC_DATE_CREATED VARCHAR(32) NOT NULL,
                                AC_LAST_MAINTAINED VARCHAR(32),
                                AC_NUM_ECONOMY INT NOT NULL,
                                AC_NUM_BUSINESS INT NOT NULL,
                                AC_NUM_FIRSTCLASS INT NOT NULL,
                                AP_ID VARCHAR(32) NOT NULL,
                                PRIMARY KEY (AC_ID),
                                FOREIGN KEY (AP_ID) REFERENCES AIRPORT(AP_ID) ON DELETE CASCADE ON UPDATE CASCADE
                                )"""

        create_flight_table = """CREATE TABLE FLIGHT (
                                F_ID INT AUTO_INCREMENT,
                                AC_ID INT NOT NULL,
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
                                FOREIGN KEY (F_DEPARTUREAIRPORTID, F_DEPARTUREGATEID) REFERENCES GATE(AP_ID, G_ID)
                                ON DELETE CASCADE ON UPDATE CASCADE,
                                FOREIGN KEY (F_ARRIVALAIRPORTID, F_ARRIVALGATEID) REFERENCES GATE(AP_ID, G_ID)
                                ON DELETE CASCADE ON UPDATE CASCADE
                                )"""

        create_employee_table = """CREATE TABLE EMPLOYEE (
                                E_ID INT AUTO_INCREMENT,
                                E_HOURS FLOAT NOT NULL,
                                E_TYPE VARCHAR(32) NOT NULL,
                                E_WAGE FLOAT NOT NULL,
                                PRIMARY KEY (E_ID)
                                )"""

        create_itinerary_table = """CREATE TABLE ITINERARY (
                                I_ID INT AUTO_INCREMENT,
                                I_SEATTYPE VARCHAR(32) NOT NULL,
                                I_SEATCOST FLOAT NOT NULL,
                                I_STATUS VARCHAR(32) NOT NULL,
                                C_ID INT NOT NULL,
                                PRIMARY KEY (I_ID),
                                FOREIGN KEY (C_ID) REFERENCES CUSTOMER(C_ID) ON DELETE CASCADE ON UPDATE CASCADE
                                )"""



        create_baggage_table = """CREATE TABLE BAGGAGE (
                                B_ID INT AUTO_INCREMENT,
                                I_ID INT NOT NULL,
                                B_WEIGHT DECIMAL(5,2) NOT NULL,
                                PRIMARY KEY (B_ID, I_ID),
                                FOREIGN KEY (I_ID) REFERENCES ITINERARY(I_ID) ON DELETE CASCADE ON UPDATE CASCADE
                                )"""

        create_frequentflier_table = """CREATE TABLE FREQUENTFLIER (
                                    C_ID INT,
                                    FF_MILES FLOAT NOT NULL,
                                    PRIMARY KEY (C_ID),
                                    FOREIGN KEY (C_ID) REFERENCES CUSTOMER(C_ID) ON DELETE CASCADE ON UPDATE CASCADE
                                    )"""

        create_workson_table = """CREATE TABLE WORKSON (
                                E_ID INT,
                                F_ID INT,
                                FOREIGN KEY (E_ID) REFERENCES EMPLOYEE(E_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                FOREIGN KEY (F_ID) REFERENCES FLIGHT(F_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                PRIMARY KEY (E_ID, F_ID)
                                )"""

        create_schedule_table = """CREATE TABLE SCHEDULE (
                                I_ID INT,
                                F_ID INT,
                                FOREIGN KEY (I_ID) REFERENCES ITINERARY(I_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                FOREIGN KEY (F_ID) REFERENCES FLIGHT(F_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                PRIMARY KEY (I_ID, F_ID)
                                )"""

        cursor.execute(create_customer_table)
        print(('Created new {0} table in {1}').format('CUSTOMER',self.db))

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

        cursor.execute(create_baggage_table)
        print(('Created new {0} table in {1}').format('BAGGAGE',self.db))

        cursor.execute(create_frequentflier_table)
        print(('Created new {0} table in {1}').format('FREQUENTFLIER',self.db))

        cursor.execute(create_workson_table)
        print(('Created new {0} table in {1}').format('WORKSON',self.db))

        cursor.execute(create_schedule_table)
        print(('Created new {0} table in {1}').format('SCHEDULE',self.db))

        print(('{0} RESET COMPLETE').format(self.db))
        cursor.close()
        db.close()
        return 0

    '''
    function: populate_db
    description: populate database with test data
    notes: do this right after reset_db()
    '''
    def populate_db(self):
        db = MySQLdb.connect(host=self.host,
                                 user=self.user,
                                 passwd=self.pw,
                                 db=self.db)
        cursor = db.cursor()

        ''' insert test customers'''
        insert_customer_1 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('TestCustomer1', 20, 'check@test.com', '6041111111')
                            """

        insert_customer_2 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('TestCustomer2', 30, 'check2@test.com', '6042222222')
                            """

        insert_customer_3 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('TestCustomer3', 40, 'check3@test.com', '6043333333')
                            """

        insert_customer_4 = """ INSERT INTO CUSTOMER (C_NAME, C_AGE, C_EMAIL, C_PHONE)
                            VALUES ('TestCustomer4', 50, 'check4@test.com', '6044444444')
                            """

        try:
            cursor.execute(insert_customer_1)
            print(('Created new {0}: {1}').format('CUSTOMER', 'TestCustomer1'))
            cursor.execute(insert_customer_2)
            print(('Created new {0}: {1}').format('CUSTOMER', 'TestCustomer2'))
            cursor.execute(insert_customer_3)
            print(('Created new {0}: {1}').format('CUSTOMER', 'TestCustomer3'))
            cursor.execute(insert_customer_4)
            print(('Created new {0}: {1}').format('CUSTOMER', 'TestCustomer4'))
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test frequentflier '''
        insert_frequentflier_1 = """ INSERT INTO FREQUENTFLIER (C_ID, FF_MILES)
                                 VALUES (1, 200.5)
                                 """
        insert_frequentflier_2 = """ INSERT INTO FREQUENTFLIER (C_ID, FF_MILES)
                                 VALUES (3, 300.5)
                                 """

        try:
            cursor.execute(insert_frequentflier_1)
            print(('Created new {0}: {1}').format('FREQUENTFLIER', 'TestCustomer1'))
            cursor.execute(insert_frequentflier_2)
            print(('Created new {0}: {1}').format('FREQUENTFLIER', 'TestCustomer3'))
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test airport '''
        insert_airport_1 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('YVR', 'VANCOUVER', 'CANADA')
                           """
        insert_airport_2 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('JFK', 'NEW YORK', 'USA')
                           """
        insert_airport_3 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('LAX', 'LOS ANGELES', 'USA')
                           """
        insert_airport_4 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('TPE', 'TAIPEI', 'TAIWAN')
                           """

        try:
            cursor.execute(insert_airport_1)
            print(('Created new {0}: {1}').format('AIRPORT', 'YVR'))
            cursor.execute(insert_airport_2)
            print(('Created new {0}: {1}').format('AIRPORT', 'JFK'))
            cursor.execute(insert_airport_3)
            print(('Created new {0}: {1}').format('AIRPORT', 'LAX'))
            cursor.execute(insert_airport_4)
            print(('Created new {0}: {1}').format('AIRPORT', 'TPE'))
            db.commit()
        except Exception as e:
            print(e)


        ''' insert test gate '''
        terminals = ['A', 'B', 'C', 'D', 'E']
        airports = ['YVR', 'JFK', 'LAX', 'TPE']
        try:
            for airport in airports:
                for t in terminals:
                    for x in range(1, 6):
                        insert_gate = """ INSERT INTO GATE(G_ID, AP_ID)
                                      VALUES('%s', '%s')
                                      """ % (t+str(x), airport)
                        cursor.execute(insert_gate)
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test aircrafts '''
        insert_aircraft_1 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('IDLE', 'BOEING777-300', 2912374.28, '07-21-1993', '10-25-2017', 300, 100, 15, 'YVR')
                            """

        insert_aircraft_2 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('INFLIGHT', 'BOEING787-10', 972172.53, '12-25-2005', '10-03-2017', 350, 100, 30, 'TPE')
                            """

        insert_aircraft_3 = """ INSERT INTO AIRCRAFT (AC_STATUS, AC_MAKE, AC_MILEAGE,
                            AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY, AC_NUM_BUSINESS,
                            AC_NUM_FIRSTCLASS, AP_ID)
                            VALUES ('INFLIGHT', 'AIRBUS A330-300', 23874536.72, '11-18-1994', '11-03-2017', 100, 50, 15, 'LAX')
                            """

        try:
            cursor.execute(insert_aircraft_1)
            print(('Created new {0} for airport: {1}').format('AIRCRAFT', 'YVR'))
            cursor.execute(insert_aircraft_2)
            print(('Created new {0} for airport: {1}').format('AIRCRAFT', 'TPE'))
            cursor.execute(insert_aircraft_3)
            print(('Created new {0} for airport: {1}').format('AIRCRAFT', 'LAX'))
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test flights '''
        insert_flight_1 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (1, 5000, '01-10-2018:23:23', '01-12-2018:06:23', 'YVR', 'TPE', 'A1', 'E5', 'PENDING')
                            """
        insert_flight_2 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (3, 250, '01-08-2018:05:23', '01-08-2018:06:23', 'LAX', 'YVR', 'C5', 'B3', 'PENDING')
                            """

        insert_flight_3 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (2, 4500, '01-13-2018:05:23', '01-13-2018:17:23', 'TPE', 'JFK', 'E2', 'A3', 'PENDING')
                            """

        try:
            cursor.execute(insert_flight_1)
            print(('Created new {0} from {1} to {2}').format('FLIGHT', 'YVR', 'TPE'))
            cursor.execute(insert_flight_2)
            print(('Created new {0} from {1} to {2}').format('FLIGHT', 'LAX', 'YVR'))
            cursor.execute(insert_flight_3)
            print(('Created new {0} from {1} to {2}').format('FLIGHT', 'TPE', 'JFK'))
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test employees '''
        insert_employee_1 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_WAGE)
                            VALUES (70, "CAPTAIN", 53)
                            """

        insert_employee_2 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_WAGE)
                            VALUES (90.5, "ATTENDANT", 35)
                            """

        insert_employee_3 = """ INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_WAGE)
                            VALUES (15, "ATTENDANT", 32)
                            """
        try:
            cursor.execute(insert_employee_1)
            print(('Created new {0}: EID = {1}').format('EMPLOYEE', 1))
            cursor.execute(insert_employee_2)
            print(('Created new {0}: EID = {1}').format('EMPLOYEE', 2))
            cursor.execute(insert_employee_3)
            print(('Created new {0}: EID = {1}').format('EMPLOYEE', 3))
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test itinerary '''
        insert_itinerary_1 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('FIRSTCLASS', 153.2, 'PENDING', 1)
                             """
        insert_itinerary_2 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('BUSINESS', 84.7, 'PENDING', 2)
                             """
        try:
            cursor.execute(insert_itinerary_1)
            print(('Created new {0}: FOR CID = {1}').format('ITINERARY', 1))
            cursor.execute(insert_itinerary_2)
            print(('Created new {0}: FOR CID = {1}').format('ITINERARY', 2))
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test baggage '''
        insert_baggage_1 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (1, 89.78)
                           """
        insert_baggage_2 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (1, 95.96)
                           """
        insert_baggage_3 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (2, 84.67)
                           """
        insert_baggage_4 = """ INSERT INTO BAGGAGE (I_ID, B_WEIGHT)
                           VALUES (2, 125.67)
                           """

        try:
            cursor.execute(insert_baggage_1)
            print(('Created new {0}: {1} onto {2}').format('BAGGAGE', 'BAGGAGE1', 'CUSTOMER1'))
            cursor.execute(insert_baggage_2)
            print(('Created new {0}: {1} onto {2}').format('BAGGAGE', 'BAGGAGE2', 'CUSTOMER1'))
            cursor.execute(insert_baggage_3)
            print(('Created new {0}: {1} onto {2}').format('BAGGAGE', 'BAGGAGE3', 'CUSTOMER2'))
            cursor.execute(insert_baggage_4)
            print(('Created new {0}: {1} onto {2}').format('BAGGAGE', 'BAGGAGE4', 'CUSTOMER3'))
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test workon '''
        insert_workon_1 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (1, 1)
                             """
        insert_workon_2 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (1, 2)
                             """
        insert_workon_3 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (1, 3)
                             """
        insert_workon_4 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (2, 1)
                             """
        insert_workon_5 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (2, 2)
                             """
        insert_workon_6 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (3, 2)
                             """
        insert_workon_7 = """ INSERT INTO WORKSON(E_ID, F_ID)
                             VALUES (3, 3)
                             """
        try:
            cursor.execute(insert_workon_1)
            cursor.execute(insert_workon_2)
            cursor.execute(insert_workon_3)
            cursor.execute(insert_workon_4)
            cursor.execute(insert_workon_5)
            cursor.execute(insert_workon_6)
            cursor.execute(insert_workon_7)
            print(('populated WORKSON table'))
            db.commit()
        except Exception as e:
            print(e)

        ''' insert test schedule '''
        insert_schedule_1 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (1, 2)
                            """
        insert_schedule_2 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (1, 1)
                            """
        insert_schedule_3 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (2, 3)
                            """
        try:
            cursor.execute(insert_schedule_1)
            cursor.execute(insert_schedule_2)
            cursor.execute(insert_schedule_3)
            print(('populated schedule table'))
            db.commit()
        except Exception as e:
            print(e)
            db.rollback()
        print(('{0} POPULATE COMPLETE').format(self.db))

        cursor.close()
        db.close()
        return 0

#==============================================================================
#   function: add_baggage
#   description: add baggage instance for cust_id
#   return: baggage json object
#==============================================================================

    def add_baggage(self, itinerary_id, bag_weight):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        add_baggage_query = """INSERT INTO BAGGAGE(I_ID, B_WEIGHT)
                                VALUES(%s, %.2f)""" % (itinerary_id, float(bag_weight))

        cursor = db.cursor()
        try:
            cursor.execute(add_baggage_query)
            db.commit()
            bag_object = {
                    'bag_id': cursor.lastrowid(),
                    'itinerary_id': itinerary_id,
                    'weight': bag_weight
                }
            data = json.dumps(bag_object, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Add Baggage Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data
    
#==============================================================================
#   function: get_baggage
#   description: returns an instance of baggage based on itinerary ID
#   return: baggage json object
#==============================================================================
    def get_baggage(self, i_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        if i_id is None:
            get_baggage_query = """SELECT * FROM BAGGAGE"""
        else:
            get_baggage_query = """SELECT * FROM BAGGAGE WHERE I_ID = %d""" % int(i_id)
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_baggage_query)
            print("query executed")
            if i_id is None:
                baggage = cursor.fetchall()
                for bag in baggage:
                    bag_object = {
                        'bag_id': bag[0],
                        'itinerary_id': bag[1],
                        'weight': str(bag[2])
                    }
                    dataList.append(bag_object)
            else:
                baggage = cursor.fetchone()
                bag_object = {
                        'bag_id': bag[0],
                        'itinerary_id': bag[1],
                        'weight': bag[2]
                    }
                dataList.append(bag_object)
                print(baggage)

            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Get Baggage Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data


#==============================================================================
#   function: get_customer
#   description: returns an instance of customer based on customer_id
#   return: customer json object
#==============================================================================
    def get_customer(self, customer_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        if (customer_id==None):
            get_customer_query = """SELECT * FROM CUSTOMER"""
        else:
            get_customer_query = """SELECT * FROM CUSTOMER
                                WHERE C_ID = %d""" % int(customer_id)
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_customer_query)
            if customer_id is None:
                customers = cursor.fetchall()
                for c in customers:
                    c_object = {
                        'customer_id': c[0],
                        'customer_name': c[1],
                        'customer_age': c[2],
                        'customer_email': c[3],
                        'customer_phone': c[4]
                    }
                    dataList.append(c_object)
            else:
                customers = cursor.fetchone()
                c_object = {
                    'customer_id': customers[0],
                    'customer_name': customers[1],
                    'customer_age': customers[2],
                    'customer_email': customers[3],
                    'customer_phone': customers[4]
                }
                dataList.append(c_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Get Customer failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_customer
#   description: adds an instance of customer to CUSTOMER table
#   return: added customer JSON object
#==============================================================================
    def add_customer(self, cust_name, cust_age, cust_email, cust_phone):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        add_customer_query = """INSERT INTO CUSTOMER(C_NAME, C_AGE, C_EMAIL, C_PHONE)
                                VALUES('%s',%d,'%s','%s')""" % (cust_name, int(cust_age),
                                cust_email, cust_phone)
        cursor = db.cursor()
        try:
            cursor.execute(add_customer_query)
            db.commit()
            customer = {
                'customer_id': cursor.lastrowid,
                'customer_name': cust_name,
                'customer_age': int(cust_age),
                'customer_email': cust_email,
                'customer_phone': cust_phone
            }
            data = json.dumps(customer, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Add Customer Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: update_customer
#   description: update the customer information
#==============================================================================
    def update_customer(self, customer_id, cust_field, new_value):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        update_customer_query = """UPDATE CUSTOMER
                                   SET %s = %s
                                   WHERE C_ID = %s""" % (cust_field, new_value, customer_id)

        cursor = db.cursor()
        try:
            cursor.execute(update_customer_query)
            db.commit()
            print('Update Customer Success')
            db.close()
            return

        except:
            print('Update Customer Failed')
            db.close()

            return 0

#==============================================================================
#   function: add_frequent_flier
#   description: adds a new frequent flier instance to FREQUENTFLIER table
#   return: added frequent flier json object
#==============================================================================
    def add_frequent_flier(self, customer_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        add_ff_query = """ INSERT INTO FREQUENTFLIER (C_ID, FF_MILES)
                           VALUES (%d, 0.0)""" % int(customer_id)

        cursor = db.cursor()
        try:
            cursor.execute(add_ff_query)
            db.commit()
            newff = {
                'customer_id': customer_id,
                'frequentflier_miles': 0.0,
            }
            data = json.dumps(newff, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Add Frequent Flier Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: update_frequent_flier
#   description: updates miles on frequent flier account
#   return: returns updated ff object
#==============================================================================
    def update_frequent_flier(self, customer_id, miles):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        cursor = db.cursor()
        try:
            cursor.execute("""SELECT FF_MILES FROM FREQUENTFLIER WHERE C_ID = %d """ % (int(customer_id)))
            old_miles = cursor.fetchone()
        except Exception as e:
            data = ("Update Frequent Flier Failed with error: {0}").format(e)
            return data

        new_miles = old_miles[0] + float(miles)
        update_ff_query = """UPDATE FREQUENTFLIER
                           SET FF_MILES = %.2f
                           WHERE C_ID = %d """ % (float(new_miles), int(customer_id))
        updated_ff = {
            'customer_id': customer_id,
            'frequentflier_miles': new_miles
        }
        try:
            cursor.execute(update_ff_query)
            db.commit()
            data = json.dumps(updated_ff, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Update Frequent Flier Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_itinerary
#   description: add a new row to ITINERARY table
#   return: added Itinerary object
#==============================================================================
    def add_itinerary(self, seat_type, seat_cost, itinerary_status, customer_id):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        add_itinerary_query = """ INSERT INTO ITINERARY (I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                              VALUES ('%s',%.2f, '%s', %d)""" % (seat_type, float(seat_cost),
                                                                itinerary_status, int(customer_id))

        cursor = db.cursor()
        try:
            cursor.execute(add_itinerary_query)
            db.commit()
            new_itinerary = {
                'itinerary_id': cursor.lastrowid,
                'seattype': seat_type,
                'seatcost': seat_cost,
                'status': itinerary_status,
                'customer_id': customer_id
            }
            data = json.dumps(new_itinerary, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Add Itinerary Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        db.close()
        cursor.close()
        return data

#==============================================================================
#   function: get_itinerary
#   description: get itinerary by customer ID
#   return: list of itineraries
#==============================================================================
    def get_itinerary(self, customer_id):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        get_itinerary_query = """SELECT * FROM ITINERARY WHERE C_ID = %s""" % customer_id
        cursor = db.cursor()

        try:
            dataList = []
            cursor.execute(get_itinerary_query)
            itineraries = cursor.fetchall()
            for itinerary in itineraries:
                it_object = {
                    'itinerary_id': itinerary[0],
                    'seattype': itinerary[1],
                    'seatcost': itinerary[2],
                    'status': itinerary[3]
                }
                dataList.append(it_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Itinerary failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: delete_itinerary
#   description: delete itinerary given itinerary ID
#   return: deleted itinerary id
#==============================================================================
    def delete_itinerary(self, itinerary_id):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        delete_itinerary_query = """ DELETE FROM ITINERARY WHERE I_ID = %d """ % int(itinerary_id)

        cursor = db.cursor()
        deleted_itinerary_id = {
            'itinerary_id': int(itinerary_id)
        }
        try:
            cursor.execute(delete_itinerary_query)
            db.commit()
            data = json.dumps(deleted_itinerary_id, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Delete Itinerary Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: update_itinerary
#   description: update itinerary fields given itinerary ID
#==============================================================================
    def update_itinerary(self, itinerary_id, itinerary_field, new_value):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        update_itinerary_query = """UPDATE ITINERARY
                                    SET %s = %s
                                    WHERE I_ID = %d """ % (itinerary_field, new_value, int(itinerary_id))

        cursor = db.cursor()
        try:
            cursor.execute(update_itinerary_query)
            db.commit()
            get_itinerary_query = """SELECT * FROM ITINERARY WHERE I_ID = %d""" % (int(itinerary_id))
            cursor.execute(get_itinerary_query)
            updated_itinerary = cursor.fetchone()
            updated_itinerary_object = {
                'itinerary_id': updated_itinerary[0],
                'seattype': updated_itinerary[1],
                'seatcost': float(updated_itinerary[2]),
                'status': updated_itinerary[3],
                'customer_id': updated_itinerary[4]
            }
            data = json.dumps(updated_itinerary_object, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Update Itinerary Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_flight
#   description: add new flight to FLIGHT table
#==============================================================================
    def add_flight(self, aircraft_id, distance, departtime, arrivetime, departairport, arriveairport,
                   departgate, arrivegate, status):
        db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.pw, db=self.db)

        add_flight_query = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE, F_DEPARTURETIME, F_ARRIVALTIME,
                               F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID, F_DEPARTUREGATEID, F_ARRIVALGATEID,
                               F_STATUS) VALUES (%d, %.2f, '%s', '%s', '%s','%s','%s','%s','%s')""" % (int(aircraft_id),
                                float(distance), departtime, arrivetime, departairport, arriveairport, departgate,
                                arrivegate, status)

        cursor = db.cursor()
        try:
            cursor.execute(add_flight_query)
            db.commit()
            new_flight = {
                'flight_id': cursor.lastrowid,
                'aircraft_id': int(aircraft_id),
                'distance': float(distance),
                'departtime': departtime,
                'arrivetime': arrivetime,
                'departairport': departairport,
                'arriveairport': arriveairport,
                'departgate': departgate,
                'arrivegate': arrivegate,
                'status': status
            }
            data = json.dumps(new_flight, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Add Flight Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: update_flight
#   description: update fields in FLIGHT given flight ID
#==============================================================================
    def update_flight(self, flight_id, flight_field, new_value):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        update_flight_query = """UPDATE FLIGHT
                                SET %s = %s
                                WHERE F_ID = %d """ % (flight_field, new_value, int(flight_id))

        cursor = db.cursor()
        try:
            cursor.execute(update_flight_query)
            db.commit()
            get_flight_query = """SELECT * FROM FLIGHT WHERE F_ID = %d""" % (int(flight_id))
            cursor.execute(get_flight_query)
            updated_flight = cursor.fetchone()
            updated_flight_object = {
                'flight_id': int(updated_flight[0]),
                'aircraft_id': int(updated_flight[1]),
                'distance': float(updated_flight[2]),
                'departtime': updated_flight[3],
                'arrivetime': updated_flight[4],
                'departairport': updated_flight[5],
                'arriveairport': updated_flight[6],
                'departgate': updated_flight[7],
                'arrivegate': updated_flight[8],
                'status': updated_flight[9]
            }
            data = json.dumps(updated_flight_object, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Update Flight Failed with error: {0}").format(e)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_flight
#   description: get all flights or a given flight ID
#   returns: the list of all flights if there are no specified Flight_id
#        or: the flight corresponding to the given Flight_id
#==============================================================================      
    def get_flight(self, f_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        get_flight_query = ""
        if f_id is None:
            get_flight_query = """SELECT * FROM FLIGHT"""
        else:
            get_flight_query = """SELECT * FROM FLIGHT WHERE F_ID = '%s'""" % (f_id)
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_flight_query)
            if f_id is None:
                flights = cursor.fetchall()
                for flight in flights:
                    f_object = {
                        'flight_id': int(flight[0]),
                        'aircraft_id': int(flight[1]),
                        'distance': float(flight[2]),
                        'departtime': flight[3],
                        'arrivetime': flight[4],
                        'departairport': flight[5],
                        'arriveairport': flight[6],
                        'departgate': flight[7],
                        'arrivegate': flight[8],
                        'status': flight[9]
                    }
                    dataList.append(f_object)
            else:
                flights = cursor.fetchone()
                f_object = {
                    'flight_id': int(flights[0]),
                        'aircraft_id': int(flights[1]),
                        'distance': float(flights[2]),
                        'departtime': flights[3],
                        'arrivetime': flights[4],
                        'departairport': flights[5],
                        'arriveairport': flights[6],
                        'departgate': flights[7],
                        'arrivegate': flights[8],
                        'status': flights[9]
                }
                dataList.append(f_object)
            data = json.dumps(dataList, sort_keys = True, indent = 4, separators = (',', ': '))
        except Exception as e:
            print("Get Flight Failed with error: {0}").format(e)
            db.rollback()
            data = 0
            
        cursor.close()
        db.close()
        return data
#==============================================================================
#   function: get_airport
#   description: get all the airports
#   returns: the list of all the airports if there are no specified Airport_id
#        or: the airport where aiport_id matches the inputted airport_id
#==============================================================================
    def get_airport(self, ap_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        get_airport_query = ""
        if ap_id is None:
            get_airport_query = """SELECT * FROM AIRPORT"""
        else:
            get_airport_query = """SELECT * FROM AIRPORT WHERE AP_ID = '%s'""" % (ap_id)
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_airport_query)
            if ap_id is None:
                airports = cursor.fetchall()
                for airport in airports:
                    ap_object = {
                        'airport_id': airport[0],
                        'city': airport[1],
                        'country': airport[2]
                    }
                    dataList.append(ap_object)
            else:
                airports = cursor.fetchone()
                ap_object = {
                    'airport_id': airports[0],
                    'city': airports[1],
                    'country': airports[2]
                }
                dataList.append(ap_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            print("Get Airport Failed with error: {0}").format(e)
            db.rollback()
            data = 0

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_airport
#   description: add an airport instance to the AIRPORT table
#==============================================================================
    def add_airport(self, ap_id, ap_city, ap_country):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        add_airport_query = """INSERT INTO AIRPORT(AP_ID, AP_CITY, AP_COUNTRY)
                                VALUES('%s', '%s', '%s')""" % (ap_id,
                                ap_city, ap_country)
        cursor = db.cursor()
        airport = {
            'airport_id': ap_id,
            'city': ap_city,
            'country': ap_country
        }
        try:
            cursor.execute(add_airport_query)
            db.commit()
            data = json.dumps(airport, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Add Airport Failed with error: {0}").format(e)
            db.rollback()

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: delete_airport
#   description: delete an airport from the airport table
#==============================================================================
    def delete_airport(self, ap_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        delete_airport_query = """DELETE FROM AIRPORT WHERE AP_ID = '%s'""" % (ap_id)
        cursor = db.cursor()
        deleted_airport_id = {
            'airport_id': ap_id
        }
        try:
            cursor.execute(delete_airport_query)
            db.commit()
            data = json.dumps(deleted_airport_id, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as e:
            data = ("Delete Airport Failed with error: {0}").format(e)
            print(data)
            db.rollback()

        cursor.close()
        db.close()
        return data

 #==============================================================================
 #   function: update_airport
 #   description: update an airport instance to the AIRPORT table
 #==============================================================================
    def update_airport(self, ap_id, field, new_value):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        update_airport_query = """UPDATE AIRPORT
                                SET %s = %s
                                WHERE AP_ID = '%s'""" % (field, new_value, ap_id)
        cursor = db.cursor()
        try:
            cursor.execute(update_airport_query)
            db.commit()
            data = ("Update Airport succeeded")
        except Exception as e:
            data = ("Update Airport Failed with error: {0}").format(e)
            print(data)
            db.rollback()

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_gates_of_airport
#   description: get all the gates from an airport
#   returns: the list of all the gates from a specified airport_id
#==============================================================================
    def get_gates_of_airport(self, ap_id):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         if ap_id is None:
             return "Airport ID is NULL"
         else:
             get_gate_query = """SELECT * FROM GATE WHERE AP_ID = '%s'""" % (ap_id)
         cursor = db.cursor()
         try:
             dataList = []
             cursor.execute(get_gate_query)
             gates = cursor.fetchall()
             for g in gates:
                 gate = {
                    'gate_id': g[0],
                    'airport_id': g[1]
                 }
                 dataList.append(gate)
             data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as e:
             data = ("Get Airport Failed with error: {0}").format(e)
             db.rollback()
             print(data)

         cursor.close()
         db.close()
         return data

#==============================================================================
#   function: delete_gate
#   description: delete a gate with specified gate id and airport id
#==============================================================================
    def delete_gate(self, ap_id, g_id):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         delete_gate_query = """DELETE FROM GATE WHERE AP_ID = '%s' and G_ID = '%s'""" % (ap_id, g_id)
         cursor = db.cursor()
         deleted_gate = {
            'airport_id': ap_id,
            'gate_id': g_id
         }
         try:
             cursor.execute(delete_gate_query)
             db.commit()
             data = json.dumps(deleted_gate, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as e:
             data = ("Delete Gate Failed with error: {0}").format(e)
             print(data)
             db.rollback()

         cursor.close()
         db.close()
         return data


#==============================================================================
#   function: add_aircraft
#   description: add an aircraft instance to table AIRCRAFT
#   returns: the added aircraft json object
#==============================================================================
    def add_aircraft(self, status, make, mileage, datecreated, lastmaintained, economy,
                    business, firstclass, airport):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        add_aircraft_query = """INSERT INTO AIRCRAFT(AC_STATUS, AC_MAKE, AC_MILEAGE,
                                AC_DATE_CREATED, AC_LAST_MAINTAINED, AC_NUM_ECONOMY,
                                AC_NUM_BUSINESS, AC_NUM_FIRSTCLASS, AP_ID)
                                VALUES ('%s', '%s', %.2f, '%s', '%s', %d, %d, %d, '%s')""" % (
                                status, make, float(mileage), datecreated, lastmaintained,
                                int(economy), int(business), int(firstclass), airport)

        cursor = db.cursor()
        try:
            cursor.execute(add_aircraft_query)
            aircraft = {
                'id': cursor.lastrowid,
                'status': status,
                'make': make,
                'mileage': float(mileage),
                'date_created': datecreated,
                'last_maintained': lastmaintained,
                'num_economy': economy,
                'num_business': business,
                'num_firstclass': firstclass,
                'airport_id': airport
            }
            db.commit()
            data = json.dumps(aircraft, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Add Aircraft Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_aircraft
#   description: get all the aircrafts with specificed aircraft_id in
#       table AIRCRAFT
#   returns: the list of all aircrafts if there are no specified aircraft_id
#        or: the aircraft where aircraft_id matches the inputted aircraft_id
#==============================================================================
    def get_aircraft(self, ac_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        if ac_id is None:
            get_aircraft_query = """SELECT * FROM AIRCRAFT"""
        else:
            get_aircraft_query = """SELECT * FROM AIRCRAFT WHERE AC_ID = %d""" % (int(ac_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_aircraft_query)
            if ac_id is None:
                aircrafts = cursor.fetchall()
                for aircraft in aircrafts:
                    ac_object = {
                        'id': aircraft[0],
                        'status': aircraft[1],
                        'make': aircraft[2],
                        'mileage': float(aircraft[3]),
                        'date_created': aircraft[4],
                        'last_maintained': aircraft[5],
                        'num_economy': aircraft[6],
                        'num_business': aircraft[7],
                        'number_firstclass': aircraft[8],
                        'airport_id': aircraft[9]
                    }
                    dataList.append(ac_object)
            else:
                aircrafts = cursor.fetchone()
                ac_object = {
                    'id': aircrafts[0],
                    'status': aircrafts[1],
                    'make': aircrafts[2],
                    'mileage': float(aircrafts[3]),
                    'date_created': aircrafts[4],
                    'last_maintained': aircrafts[5],
                    'num_economy': aircrafts[6],
                    'num_business': aircrafts[7],
                    'number_firstclass': aircrafts[8],
                    'airport_id': aircrafts[9]
                }
                dataList.append(ac_object)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Get Aircraft Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: update_aircraft
#   description: update an aircraft's status in table AIRCRAFT
#   returns: the updated aircraft object in table AIRCRAFT
#==============================================================================
    def update_aircraft(self, ac_id, status, new_status):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        if new_status is None:
            update_aircraft_query = """UPDATE AIRCRAFT SET AC_STATUS = %s
                                        WHERE AC_ID = %d""" % (status, int(ac_id))
        else:
            update_aircraft_query = """UPDATE AIRCRAFT SET AC_STATUS = %s
                                        WHERE AC_ID = %d""" % (new_status, int(ac_id))
        cursor = db.cursor()
        try:
            cursor.execute(update_aircraft_query)
            db.commit()
            get_aircraft_query = """SELECT * FROM AIRCRAFT WHERE AC_ID = %d""" % (int(ac_id))
            cursor.execute(get_aircraft_query)
            aircraft = cursor.fetchone()
            ac_object = {
                'id': aircraft[0],
                'status': aircraft[1],
                'make': aircraft[2],
                'mileage': float(aircraft[3]),
                'date_created': aircraft[4],
                'last_maintained': aircraft[5],
                'num_economy': aircraft[6],
                'num_business': aircraft[7],
                'num_firstclass': aircraft[8],
                'airport_id': aircraft[9]
            }
            data = json.dumps(ac_object, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Update Aircraft Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data


#==============================================================================
#   function: delete_aircraft
#   description: delete an aircraft from table AIRCRAFT
#   returns: the deleted aircraft id
#==============================================================================
    def delete_aircraft(self, ac_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        delete_aircraft_query = """DELETE FROM AIRCRAFT WHERE AC_ID = %d""" % (int(ac_id))
        cursor = db.cursor()
        deleted_aircraft_id = {
            'ID': ac_id
        }
        try:
            cursor.execute(delete_aircraft_query)
            db.commit()
            data = json.dumps(deleted_aircraft_id, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Delete Aircraft Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_employee
#   description: add an employee instance to table EMPLOYEE
#   returns: the added employee json object
#==============================================================================
    def add_employee(self, hours, emp_type, wage):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        add_employee_query = """INSERT INTO EMPLOYEE (E_HOURS, E_TYPE, E_WAGE)
                                VALUES (%.2f, '%s', %.2f)""" % (float(hours),
                                emp_type, float(wage))

        cursor = db.cursor()
        try:
            cursor.execute(add_employee_query)
            employee = {
                'id': cursor.lastrowid,
                'hours': float(hours),
                'type': emp_type,
                'wage': float(wage)
            }
            db.commit()
            data = json.dumps(employee, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Add Employee Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: delete_employee
#   description: delete an employee from table EMPLOYEE
#   returns: the deleted employee id
#==============================================================================
    def delete_employee(self, e_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        delete_employee_query = """DELETE FROM EMPLOYEE WHERE E_ID = %d""" % (int (e_id))
        cursor = db.cursor()
        deleted_employee_id = {
            'id': e_id
        }
        try:
            cursor.execute(delete_employee_query)
            db.commit()
            data = json.dumps(deleted_employee_id, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Delete Employee Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_schedule_for_itinerary
#   description: get all the schedules with itinerary ID
#   returns: the list of all the schedules with a specified itinerary ID
#==============================================================================
    def get_schedule_for_itinerary(self, i_id):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         if i_id is None:
             get_schedule_query = """SELECT * FROM SCHEDULE"""
         else:
             get_schedule_query = """SELECT * FROM SCHEDULE WHERE I_ID = %d""" % (int(i_id))
         cursor = db.cursor()
         try:
             dataList = []
             cursor.execute(get_schedule_query)
             if i_id is None:
                entireschedule = cursor.fetchall()
                for schedule in entireschedule:
                    s_object = {
                        'itinerary_id': schedule[0],
                        'flight_id': schedule[1]
                    }
                    dataList.append(s_object)
             else: 
                 schedule = cursor.fetchone()
                 s_object = {
                    'itinerary_id': schedule[0],
                    'flight_id': schedule[1]
                 }
                 dataList.append(s_object)
             data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as e:
             data = ("Get Schedules Failed with error: {0}").format(e)
             db.rollback()
             print(data)

         cursor.close()
         db.close()
         return data


#==============================================================================
#   function: add_workson
#   description: add an employee/flight pair instance to table workson
#   returns: the added workson json object
#==============================================================================
    def add_workson(self, e_id, f_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        add_workson_query = """INSERT INTO WORKSON VALUES (%d, %d)""" % (int(e_id),
                                int(f_id))

        cursor = db.cursor()
        workson = {
            'employee_id': e_id,
            'flight_id': f_id
        }
        try:
            cursor.execute(add_workson_query)
            db.commit()
            data = json.dumps(workson, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Add Workson Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_employee_for_flight
#   description: get all the employees on a certain flight ID in table WORKSON
#   returns: the list of all the employees with a specified flight ID
#==============================================================================
    def get_employee_for_flight(self, f_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        if f_id is None:
            return "Flight ID is NULL"
        else:
            get_employee_query = """SELECT E.E_ID
                                    FROM EMPLOYEE E, WORKSON W WHERE
                                    E.E_ID = W.E_ID AND W.F_ID = %d""" % (int(f_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_employee_query)
            employees = cursor.fetchall()
            for e in employees:
                employee = {
                    'employee_id': e
                }
                dataList.append(employee)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Get Employees Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_flight_for_employee
#   description: get all the flights for a certain employee ID in table WORKSON
#   returns: the list of all the flights for a specified employee with employee ID
#==============================================================================
    def get_flight_for_employee(self, e_id):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)
        if e_id is None:
            return "Employeesss ID is NULL"
        else:
            get_flight_query = """SELECT F.F_ID
                                    FROM FLIGHT F, WORKSON W WHERE
                                    F.F_ID = W.F_ID AND W.E_ID = %d""" % (int(e_id))
        cursor = db.cursor()
        try:
            dataList = []
            cursor.execute(get_flight_query)
            flights = cursor.fetchall()
            for f in flights:
                flight = {
                    'flight_id': f
                }
                dataList.append(flight)
            data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Get Flights Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: get_workson
#   description: gets the entire WORKSON table
#   returns: the table WORKSON
#==============================================================================
    def get_workson(self):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         get_workson_query = """SELECT * FROM WORKSON"""
         cursor = db.cursor()
         try:
             dataList = []
             cursor.execute(get_workson_query)
             worksons = cursor.fetchall()
             for w in worksons:
                 workson = {
                    'employee_id': w[0],
                    'flight_id': w[1]
                 }
                 dataList.append(workson)
             data = json.dumps(dataList, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as err:
             data = ("Get WorksOns Failed with error: {0}").format(err)
             db.rollback()
             print(data)

         cursor.close()
         db.close()
         return data

#==============================================================================
#   function: delete_workson
#   description: delete a workson relation instance from table WORKSON
#   returns: the deleted workson json object
#==============================================================================
    def delete_workson(self, e_id, f_id):
        db = MySQLdb.connect(host=self.host,
                            user=self.user,
                            passwd=self.pw,
                            db=self.db)

        delete_workson_query = """DELETE FROM WORKSON WHERE E_ID = %d and
                                F_ID = %d""" % (int (e_id), int (f_id))
        cursor = db.cursor()
        deleted_workson = {
            'employee_id': e_id,
            'flight_id': f_id
        }
        try:
            cursor.execute(delete_workson_query)
            db.commit()
            data = json.dumps(deleted_workson, sort_keys=True, indent=4, separators=(',', ': '))
        except Exception as err:
            data = 'Delete Workson Failed with error: {0}'.format(err)
            db.rollback()
            print(data)

        cursor.close()
        db.close()
        return data

#==============================================================================
#   function: add_schedule
#   description: create a schedule with a flight ID and itinerary ID
#   return: json object of added schedule
#==============================================================================
    def add_schedule(self, i_id, f_id):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         add_schedule_query = """INSERT INTO SCHEDULE VALUES (%d, %d)""" % (int(i_id), int(f_id))
         cursor = db.cursor()
         added_schedule = {
            'itinerary_id': i_id,
            'flight_id': f_id
         }
         try:
             cursor.execute(add_schedule_query)
             db.commit()
             data = json.dumps(added_schedule, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as e:
             data = ("Add Schedule Failed with error: {0}").format(e)
             print(data)
             db.rollback()

         cursor.close()
         db.close()
         return data

#==============================================================================
#   function: delete_schedule
#   description: delete a schedule with specified itinerary id and flight id
#   return: deleted schedule object
#==============================================================================
    def delete_schedule(self, i_id, f_id):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         delete_schedule_query = """DELETE FROM SCHEDULE WHERE I_ID = %d and F_ID = %d""" % (int(i_id), int(f_id))
         cursor = db.cursor()
         deleted_schedule = {
            'itinerary_id': i_id,
            'flight_id': f_id
         }
         try:
             cursor.execute(delete_schedule_query)
             db.commit()
             data = json.dumps(deleted_schedule, sort_keys=True, indent=4, separators=(',', ': '))
         except Exception as e:
             data = ("Delete Schedule Failed with error: {0}").format(e)
             print(data)
             db.rollback()

         cursor.close()
         db.close()
         return data
