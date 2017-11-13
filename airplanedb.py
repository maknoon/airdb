#!~/usr/bin/python
import MySQLdb
from flask import request
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
<<<<<<< HEAD
        db = MySQLdb.connect(host=self.host,
                                     user=self.user,
                                     passwd=self.pw,
                                     db=self.db)
        cursor = db.cursor()
=======
        cursor = MySQLdb.connect(host=self.host,
                                 user=self.user,
                                 passwd=self.pw,
                                 db=self.db).cursor()
>>>>>>> 9c87e7b4cb5b50c43094d8612ccfe84d31aa5697
        drop = 'DROP TABLE IF EXISTS {}'
        cursor.execute(drop.format('USERS'))
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
                                C_ID INT AUTO_INCREMENT,
                                C_NAME VARCHAR(32) NOT NULL,
                                C_AGE INT NOT NULL,
                                C_EMAIL VARCHAR(128) NOT NULL,
                                C_PHONE VARCHAR(32) NOT NULL,
                                PRIMARY KEY (C_ID)
                                )"""

        create_baggage_table = """CREATE TABLE BAGGAGE (
                                B_ID INT AUTO_INCREMENT,
                                C_ID INT NOT NULL,
                                B_WEIGHT DECIMAL(5,2) NOT NULL,
                                PRIMARY KEY (B_ID, C_ID),
                                FOREIGN KEY (C_ID) REFERENCES CUSTOMER(C_ID) ON DELETE CASCADE ON UPDATE CASCADE
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
                                AC_MILEAGE DECIMAL(15, 2) NOT NULL,
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
                                E_WAGE DECIMAL(5, 2) NOT NULL,
                                PRIMARY KEY (E_ID)
                                )"""

        create_itinerary_table = """CREATE TABLE ITINERARY (
                                I_ID INT AUTO_INCREMENT,
                                I_SEATTYPE VARCHAR(32) NOT NULL,
                                I_SEATCOST DECIMAL(5, 2) NOT NULL,
                                I_STATUS VARCHAR(32) NOT NULL,
                                C_ID INT NOT NULL,
                                PRIMARY KEY (I_ID),
                                FOREIGN KEY (C_ID) REFERENCES CUSTOMER(C_ID) ON DELETE CASCADE ON UPDATE CASCADE
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
                                I_ID VARCHAR(32),
                                F_ID INT,
                                FOREIGN KEY (I_ID) REFERENCES ITINERARY(I_ID) ON DELETE CASCADE ON UPDATE CASCADE,
                                FOREIGN KEY (F_ID) REFERENCES FLIGHT(F_ID) ON DELETE CASCADE ON UPDATE CASCADE,
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

        print(('{0} RESET COMPLETE').format(self.db))
        cursor.close()


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

        ''' insert test baggage '''
        insert_baggage_1 = """ INSERT INTO BAGGAGE (C_ID, B_WEIGHT)
                           VALUES (1, 89.78)
                           """
        insert_baggage_2 = """ INSERT INTO BAGGAGE (C_ID, B_WEIGHT)
                           VALUES (1, 95.96)
                           """
        insert_baggage_3 = """ INSERT INTO BAGGAGE (C_ID, B_WEIGHT)
                           VALUES (2, 84.67)
                           """
        insert_baggage_4 = """ INSERT INTO BAGGAGE (C_ID, B_WEIGHT)
                           VALUES (3, 125.67)
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


        ''' insert test airport '''
        insert_airport_1 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('YVR', 'VANCOUVER', 'CANADA')
                           """
        insert_airport_2 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('JFK', 'NEW YORK', 'USA')
                           """
        insert_airport_3 = """ INSERT INTO AIRPORT (AP_ID, AP_CITY, AP_COUNTRY)
                           VALUES ('LAX', 'LOS ANGELOS', 'USA')
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
                            VALUES (1, 5000, '01-10-2018:23:23', '01-12-2018:06:23', 'YVR', 'TPE', 'A1', 'E5', 'PEDNGING')
                            """
        insert_flight_2 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (3, 250, '01-08-2018:05:23', '01-08-2018:06:23', 'LAX', 'YVR', 'C5', 'B3', 'PEDNGING')
                            """

        insert_flight_3 = """ INSERT INTO FLIGHT (AC_ID, F_DISTANCE,
                            F_DEPARTURETIME, F_ARRIVALTIME, F_DEPARTUREAIRPORTID, F_ARRIVALAIRPORTID,
                            F_DEPARTUREGATEID, F_ARRIVALGATEID, F_STATUS)
                            VALUES (2, 4500, '01-13-2018:05:23', '01-13-2018:17:23', 'TPE', 'JFK', 'E2', 'A3', 'PEDNGING')
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
<<<<<<< HEAD
        insert_itinerary_1 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES (FIRSTCLASS', 153.2, 'PENDING', 1)
                             """
        insert_itinerary_2 = """ INSERT INTO ITINERARY(I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES (BUSINESS', 84.7, 'PENDING', 2)
=======
        insert_itinerary_1 = """ INSERT INTO ITINERARY(I_ID, I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('XMASXPECIAL', 'FIRSTCLASS', 153.2, 'PENDING', 1)
                             """
        insert_itinerary_2 = """ INSERT INTO ITINERARY(I_ID, I_SEATTYPE, I_SEATCOST, I_STATUS, C_ID)
                             VALUES ('HOLIDAYSPECIAL', 'BUSINESS', 84.7, 'PENDING', 2)
>>>>>>> 9c87e7b4cb5b50c43094d8612ccfe84d31aa5697
                             """
        try:
            cursor.execute(insert_itinerary_1)
            print(('Created new {0}: FOR CID = {1}').format('ITINERARY', 1))
            cursor.execute(insert_itinerary_2)
            print(('Created new {0}: FOR CID = {1}').format('ITINERARY', 2))
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
<<<<<<< HEAD
                            VALUES (1, 2)
                            """
        insert_schedule_2 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (1, 1)
                            """
        insert_schedule_3 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES (2, 3)
=======
                            VALUES ('XMASXPECIAL', 2)
                            """
        insert_schedule_2 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES ('XMASXPECIAL', 1)
                            """
        insert_schedule_3 = """ INSERT INTO SCHEDULE(I_ID, F_ID)
                            VALUES ('HOLIDAYSPECIAL', 3)
>>>>>>> 9c87e7b4cb5b50c43094d8612ccfe84d31aa5697
                            """
        try:
            cursor.execute(insert_schedule_1)
            cursor.execute(insert_schedule_2)
            cursor.execute(insert_schedule_3)
            print(('populated schedule table'))
            db.commit()
        except Exception as e:
            print(e)
        print(('{0} POPULATE COMPLETE').format(self.db))
        cursor.close()

#==============================================================================
#   function: update_customer
#   description: update fields in customer
#==============================================================================
    def update_customer(self, custID, field, new_value):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        update_customer_query = """UPDATE CUSTOMER
                                   SET %s = '%s'
                                   WHERE C_ID = %s""" % (field, new_value, custID)

        cursor = db.cursor()
        try:
            cursor.execute(update_customer_query)
            db.commit()
            print("Update Customer Success")
        except:
            print("Update Customer Failed")
            db.rollback()

        db.close()

#==============================================================================
#   function: add_baggage
#   description: adds an instance of baggage to BAGGAGE table
#==============================================================================
    def add_baggage(self, bag_ID, cust_ID, bag_weight):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        add_baggage_query = """INSERT INTO BAGGAGE(B_ID,C_ID,B_WEIGHT)
                                VALUES('%s','%s','%s')""" % (bag_ID, cust_ID, bag_weight)

        cursor = db.cursor()
        try:
            cursor.execute(add_baggage_query)
            db.commit()
            print("Add Baggage Success")
        except:
            print("Add Baggage Failed")
            db.rollback()

        db.close()

#==============================================================================
#   function: add_customer
#   description: adds an instance of customer to CUSTOMER table
#==============================================================================
    def add_customer(self, cust_name, cust_age, cust_email, cust_phone):
         db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

         add_customer_query = """INSERT INTO CUSTOMER(C_NAME, C_AGE, C_EMAIL, C_PHONE)
                                 VALUES('%s','%s','%s','%s')""" % (cust_name, cust_age,
                                 cust_email, cust_phone)

         cursor = db.cursor()
         try:
             cursor.execute(add_customer_query)
             db.commit()
             print("Add Customer Success")
         except:
             print("Add Customer Failed")
             db.rollback()

         db.close()

#==============================================================================
#   function: add_frequent_flier
#   description: adds a new frequent flier instance to FREQUENTFLIER table
#==============================================================================
    def add_frequent_flier(self, cust_ID, miles):
        db = MySQLdb.connect(host=self.host,
                             user=self.user,
                             passwd=self.pw,
                             db=self.db)

        add_ff_query = """INSERT INTO FREQUENTFLIER(C_ID, FF_MILES)
                          VALUES('%s', '%s')""" % (cust_ID, miles)

        cursor = db.cursor()
        try:
            cursor.execute(add_ff_query)
            db.commit()
            print("Add Frequent Flier")
        except:
            print("Add Frequent Flier Failed")
            db.rollback()

        db.close()
