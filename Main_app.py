#!/usr/bin/env python
# coding: utf-8

# In[11]:


import Validations_module as vd
import Database_connection as db_con
import Card_generate_module as cg
import Registration_process as reg_p
import Login_process as log_p


# In[12]:


import mysql.connector
from mysql.connector import Error
import pandas as pd
import random
import random
import getpass
from decimal import Decimal
import pymysql
import re


# In[13]:


def user_registration():

    print("welcome to registration page")
    print("kindly register your self to use banking facility")
    #storing input in the variable
    while True:
        res=input("Enter 'exit' to quit registration process else 1 to proceed")
        if res.lower()!='exit':
            if not reg_p.user_input():
                
                        
                    
                print("Registration unsucessful, please try again")
            else:
                print("Registration is sucessful")
        else:
            break


# In[14]:


def login_1():
    print("Please enter your details to login")
    print("enter your name")
    print("enter your password")
    name=input("name")
    password=getpass.getpass("password")

    
    connection = db_con.database_connection()
    
    try:
        with connection.cursor() as cursor:
            select_name_password="select * from banking.Users_reg_data where username=%s and password=%s"
            cursor.execute(select_name_password, (name,password))
            result = cursor.fetchall()
            #print(result[0]['UserID'])
            d_name=result[0]['UserName']
            d_pass=result[0]['password']
            user_id=result[0]['UserID']
    except Exception as e:
        print("error Occurred",e,"Please try after sometime")
        return False
    finally:
        connection.close()
    
    #print(user_id,d_name,d_pass )

    if (name.strip().lower()==d_name.lower()) & (password.strip().lower()==d_pass.lower()):
        print("login sucessfully")
        while True:
            print("please select to any below option")
        
            print("1 for check account balance")
        
            print("2 for check list of beneficiaries")
        
            print("3 for check list of cards")
        
            print("4 to add beneficiary")
        
            print("5 to update account info")
        
        
            print("6 to transfer funds")
        

        
            print("7 to change pin")
        
            print("8 to register new card")
        
            print("9 to add fund")
        
            print("10 to view transactions")
        
            print("11 to exit")
        
            response=input()
            print()
        
            if response=='1':
                d=log_p.chcek_balance(user_id)
                if not d:
                    print("balance can't be fetched")
                print("Your current account details is")
                print('Account number : ', d['Account_number'])
                print('Account Balance : ', d['Amount'])
            
                print()
        
            elif response=='2':
                if log_p.get_beneficiary(user_id):
                    print("Last request was sucessfull")
                
                    print()
      
            
            elif response=='3':
                if log_p.get_cards(user_id):
                    print("Last request was sucessfull")
                
                    print()    
            
            elif response=='4':
                print("Enter the beneficiary_name")
                b_name=input()
                while True:
                    if not vd.validate_name(b_name):
                        b_name=input("Enter the benficiary name again")
                    else:
                        break
                b_account=input("Enter the beneficairy account number")
                while True:
                    if not vd.validate_account(b_account):
                        b_account=input("Enter the beneficiary account number again")
                    else:
                        break
                bank_name=input("Enter the beneficiary bank name")
                while True:
                    if not vd.validate_bank_name(bank_name):
                        bank_name=input("enter the beneficiary bank name")
                    else:
                        break
                    
                if log_p.add_beneficiary(user_id,b_name,b_account,bank_name):
                    print("Last Transaction was sucessful")
                print()
                
            elif response=='5':
                if log_p.update_account_info(user_id):
                    print("Details updated sucessfully")
                print()
            
            elif response=='6':
                if log_p.fund_transfer(user_id):
                    print("Details updated sucessfully")
                print()
                
            elif response=='7':
                card_type=input("Enter your card type Debit , credit")
                while True:
                    if card_type.lower()=='debit' or card_type.lower()=='credit':
                        break
                    else:
                        card_type=input("Enter your card type Debit , credit")
            
                print("enter old pin")
                old_pin=log_p.enter_new_pin()
                
                print("enter new pin")
                new_pin=log_p.enter_new_pin()
                
                if log_p.change_pin(user_id, card_type, old_pin, new_pin):
                    print("Last Transaction was sucessful")
                
                print()
        
            elif response=='8':
                if log_p.reg_new_card(user_id):
                    print("Last Transaction was sucessful")
                print()        
            
            elif response=='9':
                if log_p.add_fund(user_id):
                    print("Last Transaction was sucessful")
                print()
        
            elif response=='10':
                if log_p.view_transactions(user_id):
                    print("Last Transaction was sucessful")
                print()        
            
            
            elif response=='11':
                break
                

            
    return 


# In[15]:


def main():
    while True:
        print("Welcome to Banking Application:")

        print("Enter 1 to login")
        print("Enter 2 to registration")
        print("Enter 3 to logout ")
        print()
    
        response=input("Enter your option")
        if response=='1':
            login_1()
        elif response=='2':
            user_registration()
        elif response=='3':
            print("Thank you for your time")
            break
        else:
            print("Invalid option")
            
if __name__ == "__main__":
    main()
   


# In[ ]:


#2209391278 # 9876876787

