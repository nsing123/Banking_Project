Registration Process


import mysql.connector
from mysql.connector import Error
import pandas as pd
import random
import random
import getpass
from decimal import Decimal
import pymysql
import re


# In[3]:


import Database_connection as db_con


# In[4]:


import Validations_module as vd
import Card_generate_module as cg


# In[5]:


def user_input():

    d={}
    
    # loop to endure that each filed is inserted
    for i in range(1):
        print(i)
        
        #registration process started : need required details : name, password,address,adharnumber,mobile no
        name=input("Enter your name ")
        # validation check for name
        while True:
            if not vd.validate_name(name):
                print("Enter your name again")
                name=input("Enter your name ")
            else:
                #print("Data saved")
                break
        
        d['UserName']=name
        
        password=getpass.getpass("Enter your password: ")
        # validation check for password
        while True:
            if not vd.validate_password(password):
                print("Enter your password again ,with atleast 6 charcter long including special charcter and one capital")
                password=getpass.getpass("Enter your password: ")
                continue
            else:
                break
        d['password']=password

        
        address=input("Enter your address ")
        
    #validation check for address
        while True:
            if not vd.validate_address(address):
                print("Enter your address again")
                address=input("Enter your address ")
            else:
                #print("Data saved")
                break
        d['Address']=address
        adharnumber=input("Enter your adharnumber ")
        
    #validation check for adharnumber  
        while True:
            if not vd.validate_adhar(adharnumber):
                print("Enter your adharnumber again")
                adharnumber=input("Enter your adharnumber ")

            else:
                #print("Data saved")
                break
        d['AadharNumber']=adharnumber
        
    #validation check for mobile_no 
        mobile_no=input("Enter your mobile_no ")
        while True:
            if not vd.validate_phone(mobile_no):
                print("Enter your mobile_no again")
                mobile_no=input("Enter your mobile_no ")

            else:
                #print("Data saved")
                break
        d['MobileNumber']=mobile_no
        
        if not insert_user_reg_data(name,password,address,adharnumber,mobile_no):  # if adhar number is same then do not add the record.
            return False
        
        d['account_number']=cg.generate_account()
        account_number=d['account_number']
        amount=0
        d['amount']=0

        if not insert_user_accounts(account_number,amount):
            return False
        
    
    # now generating a credit card along with pin and cvv details for each new users

        d['Credit_card']=cg.generate_card_number()
        d['C_pin']=cg.generate_pin()
        d['C_cvv']=cg.generate_cvv()
        card_type='credit'
        credit_card_number=d['Credit_card']
        credit_card_pin=d['C_pin']
        credit_card_cvv=d['C_cvv']
        
        if not insert_user_cards(card_type,credit_card_number,credit_card_pin,credit_card_cvv):
            return False
        
    # now generating a credit card along with pin and cvv details for each new users
        d['Debit_card']=cg.generate_card_number()
        d['D_pin']=cg.generate_pin()
        d['D_cvv']=cg.generate_cvv()
        card_type='debit'
        debit_card_number=d['Debit_card']
        debit_card_pin=d['D_pin']
        debit_card_cvv=d['D_cvv']
        
        if not insert_user_cards(card_type,debit_card_number,debit_card_pin,debit_card_cvv):
            return False
        
    return True # returning details to store.


# In[6]:


def insert_user_reg_data(UserName, password, Address, AadharNumber, MobileNumber):
    # Establish a connection to MySQL
    connection =db_con.database_connection()

    try:
        with connection.cursor() as cursor:
            # Define the SQL insert query with %s placeholders for parameters
            sql_insert_query = "INSERT INTO banking.Users_reg_data (UserName, password, Address, AadharNumber, MobileNumber) VALUES (%s, %s, %s, %s, %s)"
            
            # Convert amount to Decimal type (if needed)
            amount = Decimal('0.00')
            
            # Prepare data tuple for insertion
            data = (UserName, password, Address, AadharNumber, MobileNumber)
            
            # Execute the insert query with data tuple
            cursor.execute(sql_insert_query, data)
            
            # Commit the transaction
            connection.commit()
            
            #print("User registration data inserted successfully!")
            return True

    except pymysql.Error as e:
        print(f"Error inserting user registration data: {e}")
        return False

    finally:
        connection.close()  # Close the connection

# Example usage:
#insert_user_reg_data('john_doe', 'password123', '123 Main St', '123456789012', '9876543210')


# In[7]:


def insert_user_accounts(account_number,amount):
    # Establish a connection to MySQL
    connection = db_con.database_connection()

    try:
        with connection.cursor() as cursor:
            # Define the SQL insert query with %s placeholders for parameters
            
            cursor.execute("select userid from Users_reg_data order by userid desc limit 1;")
            user_id = cursor.fetchone()
            user_id=user_id["userid"]
            #print(user_id)
            
            sql_insert_query = "INSERT INTO banking.account_details (account_number,user_id,amount) VALUES (%s, %s, %s)"
            
            # Convert amount to Decimal type (if needed)
            amount = Decimal('0.00')
            
            # Prepare data tuple for insertion
            data = (account_number,user_id,amount)
            
            # Execute the insert query with data tuple
            cursor.execute(sql_insert_query, data)
            
            # Commit the transaction
            connection.commit()
            
            #print("User registration data inserted successfully!")
            return True

    except pymysql.Error as e:
        print(f"Error inserting user registration data: {e}")
        return False

    finally:
        connection.close()  # Close the connection

# Example usage:
#insert_user_reg_data('john_doe', 'password123', '123 Main St', '123456789012', '9876543210')


# In[8]:


def insert_user_cards(card_type,card_number,pin,cvv):
    # Establish a connection to MySQL
    connection =db_con.database_connection()

    try:
        with connection.cursor() as cursor:
            # Define the SQL insert query with %s placeholders for parameters
            
            cursor.execute("select userid from Users_reg_data order by userid desc limit 1;")
            user_id = cursor.fetchone()
            user_id=user_id["userid"]
            #print(user_id)
            #print(card_type,card_number,pin,cvv)
            
            sql_insert_query = "INSERT INTO banking.user_Cards (user_id,card_type,card_number,pin,cvv) VALUES (%s, %s, %s, %s, %s)"
            
            # Convert amount to Decimal type (if needed)
            amount = Decimal('0.00')
            
            # Prepare data tuple for insertion
            data = (user_id,card_type,card_number,pin,cvv)
            
            # Execute the insert query with data tuple
            cursor.execute(sql_insert_query, data)
            
            # Commit the transaction
            connection.commit()
            
            #print("User registration data inserted successfully!")
            return True

    except pymysql.Error as e:
        print(f"Error inserting user registration data: {e}")
        return False

    finally:
        connection.close()  # Close the connection





