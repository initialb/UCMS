# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode

DB_NAME = 'UCMS'

try:
	cnx = mysql.connector.connect(user='ucms',password='ucms',database=DB_NAME)
except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print("Something is wrong with your user name or password")
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
else:
	print 'Connect to MYSQL success.'
	cursor = cnx.cursor()
	tomorrow = datetime.now().date() + timedelta(days=1)

	add_employee = ("INSERT INTO employees "
               "(first_name, last_name, hire_date, gender, birth_date) "
               "VALUES (%s, %s, %s, %s, %s)")
	add_salary = ("INSERT INTO salaries "
              "(emp_no, salary, from_date, to_date) "
              "VALUES (%(emp_no)s, %(salary)s, %(from_date)s, %(to_date)s)")

	data_employee = ('Geert', 'Vanderkelen', tomorrow, 'M', date(1977, 6, 14))

	# Insert new employee
	cursor.execute(add_employee, data_employee)
	emp_no = cursor.lastrowid

	# Insert salary information
	data_salary = {
	  'emp_no': emp_no,
	  'salary': 50000,
	  'from_date': tomorrow,
	  'to_date': date(9999, 1, 1),
	}
	cursor.execute(add_salary, data_salary)

	# Make sure data is committed to the database
	cnx.commit()

	cursor.close()
	cnx.close()

