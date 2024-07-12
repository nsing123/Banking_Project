#database connection module

def database_connection():
    connection=None
    try:
        connection=    pymysql.connect(host='localhost',
                                 user='root',
                                 password='Mar23iscming',
                                 database='banking',
                                 cursorclass=pymysql.cursors.DictCursor) # this connection for retriving data from sql in form of dictionary
        #print("MySQL datyabase is connected suscessfully")
    except Error as err:
        print(f"Error :{err}")
    return connection
def create_db_connection():
    connection=None
    try:
        connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mar23iscming",
        database="Banking"
        ) ## this connection for retriving data from sql in form of tuple
        #print("MySQL datyabase is connected suscessfully")
    except Error as err:
        print(f"Error :{err}")
    return connection
import mysql.connector
from mysql.connector import Error

import pymysql
def create_server_connection(host_name,user_name,user_password):
    connection=None
    try:
        connection=mysql.connector.connect(host=host_name,
                                          user=user_name,
                                          password=user_password
                                          )
        print("MYSQL Database is connected sucessfully")
    except Error as err:
            print(f"Error: {err}")
    return connection

pw="enter your password" #enter your password
db="database name" #database name
connection=create_server_connection("localhost","root",pw)
def create_db_connection():
    connection=None
    try:
        connection=mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mar23iscming",
        database="Banking"
        )
        #print("MySQL datyabase is connected suscessfully")
    except Error as err:
        print(f"Error :{err}")
    return connection

def execute_query(connection,query):
    cursor=connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query was sucessful")
    except Error as err:
        print(f"Error : {err}")
def read_query(connection,query):
    cursor=connection.cursor()
    result=None
    try:
        cursor.execute(query)
        result=cursor.fetchall()
        return result
    except Error as err:
        print(f"Error : {err}")
    finally:
        connection.close()

                       

