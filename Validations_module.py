#!/usr/bin/env python
# coding: utf-8

# In[13]:


import mysql.connector
from mysql.connector import Error
import pandas as pd
import random
import random
import getpass
from decimal import Decimal
import pymysql
import re
"""
Validation logic each string is check if it is null or not.
then according to field its valid datatype is checked.

"""
def validate_name(name):
    if len(name)=="":
        return False
    elif len(name)<3:
        return False
    elif not re.match(r'^[a-zA-Z ]+$', name):
        return False
    else:
        return True

def validate_address(name):
    # Regular expression to match a basic postal address format
    address_pattern = r'^[\w\d\s#,./-]+$'

    # Compile the regular expression pattern
    regex = re.compile(address_pattern)

    # Check if the address matches the pattern
    if all([i.isdigit() for i in name.split()]):
        return False
    elif len(name)<3:
        return False
    elif regex.match(name):
        return True
    else:
        return False

def validate_adhar(name):
    if len(name)=="":
        return False
    elif len(str(name))!=12:
        return False
    elif str(name)[0]=='0':
        return False
    elif not str(name).isdigit():
        return False
    else:
        return True
def validate_phone(name):
    if len(name)=="":
        return False
    elif not re.match(r'^(\+91|91|0)?\d{10}$', name):
        return False
    else:
        return True

def validate_account(account_number):
    # Regular expression to match a 10-digit numeric account number
    pattern = r'^\d{10}$'
    
    if re.match(pattern, account_number):
        return True
    else:
        return False
    
def validate_pin(pin):
    # Check if PIN is exactly 4 digits long and consists only of digits
    if len(pin) != 4 or not pin.isdigit():
        return False
    else:
        return True
def validate_cvv(cvv):
    # Check if PIN is exactly 4 digits long and consists only of digits
    if len(pin) != 3 or not pin.isdigit():
        return False
    else:
        return True
def validate_bank_name(bank_name):
    # Regular expression to match a basic bank name format
    # Adjust as per your specific validation requirements
    bank_name_pattern = r'^[a-zA-Z\s\-\&\.\'\(\)]+$'

    # Compile the regular expression pattern
    regex = re.compile(bank_name_pattern)

    # Check if the bank name matches the pattern and is not empty
    if regex.match(bank_name) and len(bank_name.strip()) > 0:
        return True
    else:
        return False
def validate_password(password):
    # Check length
    if len(password) < 6:
        return False
    
    # Check for at least one uppercase letter
    if not any(char.isupper() for char in password):
        return False
    
    # Check for at least one special character
    special_chars = "!@#$%^&*()-_+=[]{};:'\"\\|,.<>/?"
    if not any(char in special_chars for char in password):
        return False
    
    # If all checks pass, return True
    return True


# In[ ]:




