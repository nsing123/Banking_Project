#!/usr/bin/env python
# coding: utf-8

# In[28]:


import mysql.connector
from mysql.connector import Error
import pandas as pd
import random
import random
import getpass
from decimal import Decimal
import pymysql
import re


# In[29]:


import Database_connection as db_con


# In[30]:


# genertaing account number and validate at  database end
def generate_account():
    account_number=''.join([str(random.randint(0, 9)) for _ in range(10)])
    d_acc=db_con.read_query(db_con.create_db_connection(),"select Account_number from banking.account_details")
    if (account_number.strip().lower() not in [i[0].strip().lower() for i in d_acc]):
        #print("account",account_number)
        return account_number

# genertaing 16 digit card number and validate at  database end
def generate_card_number():
        first_digit = random.randint(1, 9)
        card_number=str(first_digit) + ''.join([str(random.randint(0, 9)) for _ in range(15)])
        d_credit_card=db_con.read_query(db_con.create_db_connection(),"select card_number from banking.user_Cards")
        d_debit_card=db_con.read_query(db_con.create_db_connection(),"select card_number from banking.user_Cards")
        
        if (card_number.strip().lower() not in [i[0].strip().lower() for i in d_credit_card]) & (card_number.strip().lower() not in [i[0].strip().lower() for i in d_debit_card]):
            return card_number
        
# generating 4 digit pin and validate at  database end   
def generate_pin():
        pin=''.join([str(random.randint(0, 9)) for i in range(4)])
        d_credit_pin=db_con.read_query(db_con.create_db_connection(),"select pin from banking.user_Cards")
        d_debit_pin=db_con.read_query(db_con.create_db_connection(),"select pin from banking.user_Cards")
        if (pin.strip().lower() not in [i[0].strip().lower() for i in d_credit_pin]) & (pin.strip().lower() not in [i[0].strip().lower() for i in d_debit_pin]):
            return pin

# generate 3 digit cvv and validate at  database end
def generate_cvv():
        cvv=''.join([str(random.randint(0, 9)) for i in range(3)])
        d_credit_cvv=db_con.read_query(db_con.create_db_connection(),"select cvv from banking.user_Cards")
        d_debit_cvv=db_con.read_query(db_con.create_db_connection(),"select cvv from banking.user_Cards")
        if (cvv.strip().lower() not in [i[0].strip().lower() for i in d_credit_cvv]) & (cvv.strip().lower() not in [i[0].strip().lower() for i in d_debit_cvv]):
            return cvv


